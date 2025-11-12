"""Parallel orchestrator with DAG-based wave execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time
import uuid

from src.core.base import BaseFunctionalAgent, BaseAdvisor
from src.core.types import AgentOutput
from src.core.memory import SharedMemory
from src.core.resume import CheckpointStore, Checkpoint
from .hooks import PostStepHook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class PipelineStep:
    """Pipeline step with dependencies and category support."""

    stage: str
    agent: str
    advisor: str
    task: str
    category: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)
    max_retries: int = 0


class OrchestratorParallel:
    """
    Orchestrator that executes a pipeline in dependency waves:
    - Each wave executes steps whose deps are satisfied
    - Within a wave, steps run in parallel (thread-safe SharedMemory)
    - Honors per-category score thresholds (policy)
    """

    def __init__(
        self,
        agent_factory: Callable[[str], BaseFunctionalAgent],
        advisor_factory: Callable[[str], BaseAdvisor],
        checkpoint_store: Optional[CheckpointStore] = None,
        max_workers: int = 4,
        score_thresholds: Optional[Dict[str, float]] = None,
        post_step_hooks: Optional[Sequence[PostStepHook]] = None,
    ) -> None:
        """
        Initialize parallel orchestrator.
        
        Args:
            agent_factory: Factory function for creating agents
            advisor_factory: Factory function for creating advisors
            checkpoint_store: Optional checkpoint store
            max_workers: Max parallel workers per wave
            score_thresholds: Category -> min score mapping
        """
        self.agent_factory = agent_factory
        self.advisor_factory = advisor_factory
        self.memory = SharedMemory()
        self.checkpoints = checkpoint_store or CheckpointStore()
        self.run_id = str(uuid.uuid4())
        self.max_workers = max_workers
        self.score_thresholds = score_thresholds or {}
        self.post_step_hooks = list(post_step_hooks or [])

    def _render_task(self, template: str) -> str:
        """Render task template with memory values."""
        task = template
        snap = self.memory.to_dict()

        for k, v in snap.items():
            tok = "{" + k + "}"
            if tok in task:
                task = task.replace(tok, str(v))

        return task

    def _exec_step(self, step: PipelineStep) -> Dict[str, Any]:
        """Execute a single pipeline step."""
        stage_start = time.time()

        agent = self.agent_factory(step.agent)
        advisor = self.advisor_factory(step.advisor)

        # Category-aware threshold override
        if step.category and step.category in self.score_thresholds:
            agent.min_advisor_score = float(self.score_thresholds[step.category])
            logger.info(
                f"[{step.stage}] threshold={agent.min_advisor_score:.2f} "
                f"(category={step.category})"
            )

        task = self._render_task(step.task)

        attempt = 0
        latest_output: Optional[AgentOutput] = None
        latest_review: Optional[Dict[str, Any]] = None

        while attempt <= step.max_retries:
            attempt += 1

            output = agent.process(task=task, context=self.memory.to_dict())
            agent.validate_output(output)
            latest_output = output

            review = advisor.review(
                output=output, task=task, context=self.memory.to_dict()
            )
            latest_review = review

            if advisor.gate(review, agent.min_advisor_score):
                logger.info(
                    f"[{step.stage}] Approved score={review['score']:.2f}"
                )
                break

            logger.warning(
                f"[{step.stage}] Rejected {attempt}/{step.max_retries+1} "
                f"score={review['score']:.2f}"
            )
            if attempt > step.max_retries:
                break

            # Feed back suggestions/issues into memory
            self.memory.update(
                {
                    f"{step.stage}.last_review": review,
                    f"{step.stage}.last_output": output.to_dict(),
                }
            )

        # Persist outcome
        if latest_output:
            self.memory.update(
                {
                    f"{step.stage}.content": latest_output.content,
                    f"{step.stage}.artifacts": [
                        a.to_dict() for a in latest_output.artifacts
                    ],
                    f"{step.stage}.metadata": latest_output.metadata.to_dict(),
                    f"{step.stage}.review": latest_review,
                }
            )

        self.checkpoints.save(
            key=f"{self.run_id}:{step.stage}",
            checkpoint=Checkpoint(
                run_id=self.run_id,
                step_index=-1,
                stage=step.stage,
                memory_snapshot=self.memory.to_dict(),
                extra={"duration_ms": int((time.time() - stage_start) * 1000)},
            ),
        )

        summary = {
            "stage": step.stage,
            "agent": step.agent,
            "advisor": step.advisor,
            "approved": bool(
                latest_review and latest_review.get("approved", False)
            ),
            "score": float(latest_review["score"]) if latest_review else 0.0,
            "category": step.category or "default",
        }

        # Hooks run **after** checkpoint: safe to mutate memory for downstream waves
        for hook in self.post_step_hooks:
            hook(step_result=summary, shared_memory=self.memory)

        return summary

    def run_waves(self, steps: List[PipelineStep]) -> Dict[str, Any]:
        """
        Execute pipeline steps in dependency waves (parallel within wave).
        
        Args:
            steps: List of pipeline steps with dependencies
            
        Returns:
            Dict with run_id, history, and memory snapshot
            
        Raises:
            RuntimeError: If cyclic or unsatisfied dependencies detected
        """
        # Build dependency graph
        by_name = {s.stage: s for s in steps}
        indeg: Dict[str, int] = {s.stage: 0 for s in steps}
        edges: Dict[str, List[str]] = {s.stage: [] for s in steps}

        for s in steps:
            for d in (s.depends_on or []):
                indeg[s.stage] += 1
                edges.setdefault(d, []).append(s.stage)

        # Wave scheduling
        history: List[Dict[str, Any]] = []
        ready: List[str] = [n for n, deg in indeg.items() if deg == 0]
        visited: Set[str] = set()

        while ready:
            wave = ready[:]
            ready.clear()

            logger.info(f"[WAVE] Executing stages in parallel: {wave}")

            # Parallel execution within wave
            with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
                futs = {exe.submit(self._exec_step, by_name[n]): n for n in wave}
                for fut in as_completed(futs):
                    res = fut.result()
                    history.append(res)
                    visited.add(res["stage"])

            # Reduce indegree for next wave
            for n in wave:
                for v in edges.get(n, []):
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        ready.append(v)

        if len(visited) != len(steps):
            missing = [s.stage for s in steps if s.stage not in visited]
            raise RuntimeError(
                f"Cyclic or unsatisfied dependencies for: {missing}"
            )

        return {
            "run_id": self.run_id,
            "history": history,
            "memory": self.memory.to_dict(),
        }

