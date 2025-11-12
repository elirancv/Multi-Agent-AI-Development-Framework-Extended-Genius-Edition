"""Orchestrator for executing multi-agent pipelines."""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence

from src.core.base import BaseAdvisor, BaseFunctionalAgent
from src.core.memory import SharedMemory
from src.core.resume import Checkpoint, CheckpointStore
from src.core.types import AgentOutput

from .budget import Budget, BudgetExceededError, enforce_budget
from .cache import AgentCache
from .errors import (
    ExhaustedRetriesError,
    InvalidOutputError,
    TimeoutOrchestratorError,
)
from .eventlog import JsonlEventLog
from .hooks import PostStepHook
from .otel import span
from .seed import seed_for
from .task_render import render_task
from .timeout import FutureTimeoutError, run_with_timeout

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class PipelineStep:
    """Single pipeline step: agent name, advisor name, stage, and task template."""

    stage: str
    agent: str
    advisor: str
    task: str  # plain text or templated string using memory keys
    max_retries: int = 1  # advisor-gated retries
    category: Optional[str] = None  # Category for policy threshold lookup


class Orchestrator:
    """
    Minimal orchestrator:
    - Renders task from shared memory
    - Executes agent
    - Runs 1:1 advisor
    - Retries if not approved or score < min threshold
    - Saves checkpoints
    - Supports policy-based score thresholds per category
    """

    def __init__(
        self,
        agent_factory: Callable[[str], BaseFunctionalAgent],
        advisor_factory: Callable[[str], BaseAdvisor],
        checkpoint_store: Optional[CheckpointStore] = None,
        post_step_hooks: Optional[Sequence[PostStepHook]] = None,
    ) -> None:
        self.agent_factory = agent_factory
        self.advisor_factory = advisor_factory
        self.memory = SharedMemory()
        # Use filesystem checkpoint store by default for persistence
        if checkpoint_store is None:
            from .checkpoint_fs import FileCheckpointStore

            self.checkpoints = FileCheckpointStore()
        else:
            self.checkpoints = checkpoint_store
        self.run_id = str(uuid.uuid4())
        self.policy: Optional[Any] = None  # Policy from YAML loader
        self.post_step_hooks = list(post_step_hooks or [])
        self.eventlog = JsonlEventLog(path=f"out/{self.run_id}_events.jsonl")
        self.cache = AgentCache()
        self.agent_timeout_sec: float = 60.0  # Configurable timeout (can be overridden by policy)
        self.use_cache: bool = True  # Can be disabled via --no-cache flag
        self.start_time: float = time.time()  # Track runtime for budget
        self.budget: Optional[Budget] = None  # Budget from policy
        self.total_artifacts_bytes: int = 0  # Track total artifacts size for budget

    def _render_task(self, template: str, memory: SharedMemory) -> str:
        """Render task template with memory values."""
        return render_task(template, memory.to_dict())

    def run(self, steps: List[PipelineStep]) -> Dict[str, Any]:
        """Execute pipeline steps with retry logic and checkpointing."""
        history: List[Dict[str, Any]] = []

        for idx, step in enumerate(steps):
            stage_start = time.time()

            # Save previous content for diff comparison (before overwriting)
            prev_content = self.memory.get(f"{step.stage}.content")
            if prev_content is not None:
                self.memory.set(f"{step.stage}.previous_content", prev_content)

            # Set deterministic seed for reproducibility
            seed_for(self.run_id, step.stage)

            # Wrap step execution in OpenTelemetry span
            with span(
                "step",
                {
                    "run_id": self.run_id,
                    "stage": step.stage,
                    "agent": step.agent,
                    "category": step.category or "default",
                },
            ):
                agent = self.agent_factory(step.agent)
                task = self._render_task(step.task, self.memory)

            self.eventlog.emit(
                "step_start",
                run_id=self.run_id,
                stage=step.stage,
                agent=step.agent,
                advisor=step.advisor,
            )

            # Apply policy-driven timeouts and retries
            current_timeout = self.agent_timeout_sec
            if self.policy and step.category:
                policy_timeout = getattr(self.policy, "timeouts", {}).get(step.category)
                if policy_timeout is not None:
                    current_timeout = float(policy_timeout)
                    logger.info(
                        f"[{step.stage}] Using policy timeout {current_timeout:.1f}s "
                        f"for category '{step.category}'"
                    )

                policy_retries = getattr(self.policy, "retries", {}).get(step.category)
                if policy_retries is not None and step.max_retries == 0:
                    step.max_retries = int(policy_retries)
                    logger.info(
                        f"[{step.stage}] Using policy retries {step.max_retries} "
                        f"for category '{step.category}'"
                    )

            # Check if council is configured for this category
            advisor = None
            if self.policy and step.category:
                advisor_cfg = getattr(self.policy, "advisors", {}).get(step.category)
                if advisor_cfg:
                    from .council import AdvisorCouncil

                    advisor = AdvisorCouncil(
                        advisor_factory=self.advisor_factory,
                        advisors=list(advisor_cfg.get("list", [])),
                        decision=str(advisor_cfg.get("decision", "majority")),
                        min_score=agent.min_advisor_score,
                        weights=advisor_cfg.get("weights"),  # Pass weights from policy
                    )
                    logger.info(
                        f"[{step.stage}] Using AdvisorCouncil with {len(advisor_cfg.get('list', []))} advisors "
                        f"(decision={advisor_cfg.get('decision', 'majority')})"
                    )

            # Fallback to single advisor if no council configured
            if advisor is None:
                advisor = self.advisor_factory(step.advisor)

            advisor_name = getattr(advisor, "name", "AdvisorCouncil")
            logger.info(f"[{step.stage}] Running {agent.describe()} with advisor {advisor_name}")

            attempt = 0
            latest_output: Optional[AgentOutput] = None
            latest_review: Optional[Dict[str, Any]] = None
            error_reason: Optional[str] = None

            # Determine threshold: policy category > agent default
            threshold = agent.min_advisor_score
            if self.policy and step.category:
                policy_threshold = self.policy.score_thresholds.get(step.category)
                if policy_threshold is not None:
                    threshold = policy_threshold
                    logger.info(
                        f"[{step.stage}] Using policy threshold {threshold:.2f} "
                        f"for category '{step.category}'"
                    )

            while attempt <= step.max_retries:
                attempt += 1

                self.eventlog.emit(
                    "step_attempt",
                    run_id=self.run_id,
                    stage=step.stage,
                    attempt=attempt,
                    max_retries=step.max_retries,
                )

                # Use consistent variable for current output
                current_output: Optional[AgentOutput] = None

                # Check cache first (if enabled, include agent version for cache invalidation)
                agent_version = getattr(agent, "version", "0.1.0")
                cached = None
                if self.use_cache:
                    cached = self.cache.get(
                        agent.name, step.stage, task, self.memory.to_dict(), agent_version
                    )
                if cached:
                    # Hydrate memory from cache
                    self.memory.update(
                        {
                            f"{step.stage}.content": cached["content"],
                            f"{step.stage}.artifacts": cached.get("artifacts", []),
                            f"{step.stage}.metadata": cached.get("metadata", {}),
                        }
                    )
                    # Reconstruct AgentOutput from cache for validation
                    from src.core.types import AgentMetadata, Artifact

                    artifacts = [Artifact(**a) for a in cached.get("artifacts", [])]
                    metadata = AgentMetadata(**cached.get("metadata", {}))
                    current_output = AgentOutput(
                        content=cached["content"],
                        artifacts=artifacts,
                        metadata=metadata,
                    )
                    latest_output = current_output
                    self.eventlog.emit(
                        "cache_hit",
                        run_id=self.run_id,
                        stage=step.stage,
                        agent=agent.name,
                    )
                else:
                    # Run agent with timeout
                    def _agent_call() -> AgentOutput:
                        return agent.process(task=task, context=self.memory.to_dict())

                    try:
                        output = run_with_timeout(_agent_call, current_timeout)
                        agent.validate_output(output)
                        current_output = output
                        latest_output = output

                        # Cache the result (include agent version)
                        self.cache.put(
                            agent.name,
                            step.stage,
                            task,
                            self.memory.to_dict(),
                            output.to_dict(),
                            agent_version,
                        )
                    except FutureTimeoutError as e:
                        logger.error(f"[{step.stage}] Agent timeout after {current_timeout}s")
                        error_reason = TimeoutOrchestratorError.reason
                        self.eventlog.emit(
                            "error",
                            run_id=self.run_id,
                            stage=step.stage,
                            reason=error_reason,
                            timeout_sec=current_timeout,
                        )
                        raise TimeoutOrchestratorError(
                            f"Agent timeout after {current_timeout}s"
                        ) from e
                    except (TypeError, ValueError) as e:
                        error_reason = InvalidOutputError.reason
                        self.eventlog.emit(
                            "error",
                            run_id=self.run_id,
                            stage=step.stage,
                            reason=error_reason,
                        )
                        raise InvalidOutputError(str(e)) from e

                # Always use current_output (works for both cache and fresh execution)
                review = advisor.review(
                    output=current_output, task=task, context=self.memory.to_dict()
                )
                latest_review = review

                if advisor.gate(review, threshold):
                    logger.info(
                        f"[{step.stage}] Approved: score={review['score']:.2f} "
                        f"(threshold={threshold:.2f})"
                    )
                    break
                else:
                    logger.warning(
                        f"[{step.stage}] Rejected attempt {attempt}/{step.max_retries+1} "
                        f"(score={review['score']:.2f})"
                    )
                    self.eventlog.emit(
                        "step_rejected",
                        run_id=self.run_id,
                        stage=step.stage,
                        attempt=attempt,
                        score=float(review["score"]),
                        threshold=threshold,
                    )
                    if attempt > step.max_retries:
                        logger.error(f"[{step.stage}] Exhausted retries.")
                        error_reason = ExhaustedRetriesError.reason
                        self.eventlog.emit(
                            "error",
                            run_id=self.run_id,
                            stage=step.stage,
                            reason=error_reason,
                            attempts=attempt,
                        )
                        break

                    # Minimal refine loop: inject suggestions/issues back into memory
                    self.memory.update(
                        {
                            f"{step.stage}.last_review": review,
                            f"{step.stage}.last_output": output.to_dict(),
                        }
                    )

            # Persist memory and checkpoint after the step
            if latest_output:
                self.memory.update(
                    {
                        f"{step.stage}.content": latest_output.content,
                        f"{step.stage}.artifacts": [a.to_dict() for a in latest_output.artifacts],
                        f"{step.stage}.metadata": latest_output.metadata.to_dict(),
                        f"{step.stage}.review": latest_review,
                    }
                )

            self.checkpoints.save(
                key=f"{self.run_id}:{idx}",
                checkpoint=Checkpoint(
                    run_id=self.run_id,
                    step_index=idx,
                    stage=step.stage,
                    memory_snapshot=self.memory.to_dict(),
                    extra={"duration_ms": int((time.time() - stage_start) * 1000)},
                ),
            )

            step_summary = {
                "stage": step.stage,
                "agent": step.agent,
                "advisor": step.advisor,
                "category": step.category or "default",
                "approved": bool(latest_review and latest_review.get("approved", False)),
                "score": float(latest_review["score"]) if latest_review else 0.0,
                "error_reason": error_reason,
            }
            history.append(step_summary)

            # Call post-step hooks
            for hook in self.post_step_hooks:
                hook(step_result=step_summary, shared_memory=self.memory)

            # Enforce budget after each stage
            if self.budget:
                # Calculate artifacts size for this stage and accumulate
                if latest_output:
                    for artifact in latest_output.artifacts:
                        # Estimate size (rough approximation)
                        self.total_artifacts_bytes += len(artifact.name.encode("utf-8"))
                        if hasattr(artifact, "content") and artifact.content:
                            data = artifact.content
                            if isinstance(data, bytes):
                                self.total_artifacts_bytes += len(data)
                            else:
                                self.total_artifacts_bytes += len(str(data).encode("utf-8"))

                stats = {
                    "stages": len(history),
                    "artifacts_bytes": self.total_artifacts_bytes,
                    "runtime_sec": time.time() - self.start_time,
                }
                try:
                    enforce_budget(self.budget, stats)
                except BudgetExceededError as e:
                    logger.error(f"[BUDGET] {e}")
                    raise

        return {
            "run_id": self.run_id,
            "history": history,
            "memory": self.memory.to_dict(),
        }
