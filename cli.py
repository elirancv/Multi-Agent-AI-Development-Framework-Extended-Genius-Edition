"""CLI for running multi-agent pipelines from YAML."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from src.orchestrator.runner import Orchestrator
from src.orchestrator.runner_parallel import OrchestratorParallel
from src.orchestrator.factory import agent_factory, advisor_factory
from src.orchestrator.hooks import PromptRefinerOnFailure
from src.orchestrator.report import build_markdown_report
from src.orchestrator.artifact_sink import persist_artifacts
from src.orchestrator.yaml_loader import (
    YAMLPipelineLoader,
    PipelineValidationError,
)
from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict


def parse_kv_pairs(pairs: list[str]) -> Dict[str, Any]:
    """Parse key=value pairs from CLI, supporting JSON values."""
    out: Dict[str, Any] = {}
    for p in pairs or []:
        if "=" not in p:
            raise ValueError(f"Invalid --mem '{p}', expected key=value")
        k, v = p.split("=", 1)
        try:
            out[k] = json.loads(v)
        except json.JSONDecodeError:
            out[k] = v
    return out


def main() -> None:
    """Main CLI entry point."""
    ap = argparse.ArgumentParser(
        description="Run multi-agent pipeline from YAML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --pipeline pipeline/example.yaml
  python cli.py --pipeline pipeline/example.yaml --mem product_idea='"eBay template"' stage='"requirements"'
  python cli.py --pipeline pipeline/example.yaml --mem product_idea='"Test"' --fail-fast
        """,
    )
    ap.add_argument(
        "--pipeline",
        required=False,
        help="Path to YAML pipeline file",
    )
    ap.add_argument(
        "--mem",
        nargs="*",
        help="Memory seed overrides: key=value (JSON values allowed, use quotes)",
    )
    ap.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first rejection",
    )
    ap.add_argument(
        "--output",
        choices=["json", "human"],
        default="human",
        help="Output format: human (markdown report, default) or json",
    )
    ap.add_argument(
        "--parallel",
        action="store_true",
        help="Use parallel orchestrator (wave-based execution)",
    )
    ap.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Max parallel workers (only with --parallel)",
    )
    ap.add_argument(
        "--refine-on-fail",
        action="store_true",
        help="Auto-run PromptRefiner on failed steps",
    )
    ap.add_argument(
        "--save-artifacts",
        action="store_true",
        help="Save artifacts to filesystem (out/<run_id>/<stage>/)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate YAML only and exit (no execution)",
    )
    ap.add_argument(
        "--otel-endpoint",
        type=str,
        help="OpenTelemetry OTLP HTTP endpoint (e.g., http://localhost:4318/v1/traces)",
    )
    ap.add_argument(
        "--otel-service",
        type=str,
        default="multi-agent",
        help="Service name for OpenTelemetry traces",
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable agent output caching",
    )
    ap.add_argument(
        "--top-suggestions",
        action="store_true",
        help="Include top 5 suggestions summary in report",
    )
    ap.add_argument(
        "--export-graph",
        type=str,
        help="Export pipeline graph (DOT) to the given path; only used with --dry-run",
    )
    ap.add_argument(
        "--resume-run-id",
        type=str,
        help="Resume from a previous run ID (loads the latest checkpoint memory)",
    )
    ap.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit",
    )
    ap.add_argument(
        "--checkpoint-store",
        choices=["fs", "sqlite"],
        default="fs",
        help="Checkpoint store backend: fs (filesystem) or sqlite (default: fs)",
    )
    ap.add_argument(
        "--preset",
        type=str,
        help="Use preset configuration (e.g., 'mvp-fast', 'production', 'research')",
    )

    args = ap.parse_args()
    
    # Handle --version
    if args.version:
        from src import __version__
        print(__version__)
        sys.exit(0)
    
    # Pipeline is required for all other operations
    if not args.pipeline:
        ap.error("--pipeline is required (use --version to print version)")
    
    # Setup structured logging if needed
    from src.orchestrator.logging import setup_logging
    setup_logging()

    # Dry-run mode: validate and exit
    if args.dry_run:
        from src.orchestrator.dryrun import validate_pipeline_file

        try:
            n, names = validate_pipeline_file(args.pipeline)
            
            # Export graph if requested
            if args.export_graph:
                from src.orchestrator.graph import pipeline_to_dot
                from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict
                
                loader = YAMLPipelineLoaderStrict()
                steps, _ = loader.load(args.pipeline)
                dot = pipeline_to_dot(steps)
                dot.save(args.export_graph)
                print(f"Graph exported to {args.export_graph}", file=sys.stderr)
            
            print(
                json.dumps(
                    {
                        "pipeline": args.pipeline,
                        "stages": n,
                        "order": names,
                        "status": "valid",
                    },
                    indent=2,
                )
            )
            sys.exit(0)
        except Exception as e:
            print(
                json.dumps(
                    {
                        "pipeline": args.pipeline,
                        "status": "invalid",
                        "error": str(e),
                    },
                    indent=2,
                ),
                file=sys.stderr,
            )
            sys.exit(1)

    # Initialize OpenTelemetry if endpoint provided
    if args.otel_endpoint:
        from src.orchestrator.otel import init_otel
        init_otel(args.otel_service, args.otel_endpoint)

    try:
        # Load pipeline (use strict loader if parallel, regular otherwise)
        if args.parallel:
            loader = YAMLPipelineLoaderStrict()
            steps, score_thresholds = loader.load(args.pipeline)
        else:
            loader = YAMLPipelineLoader()
            steps, policy = loader.load_from_file(args.pipeline)

        # Setup post-step hooks
        post_hooks = []
        if args.refine_on_fail:
            post_hooks.append(
                PromptRefinerOnFailure(
                    agent_factory=agent_factory, advisor_factory=advisor_factory
                )
            )

        # Load preset if specified
        if args.preset:
            from src.orchestrator.preset_loader import load_preset
            preset_policy = load_preset(args.preset)
            if preset_policy and policy:
                # Merge preset into policy (pipeline values override preset)
                if preset_policy.score_thresholds:
                    for cat, threshold in preset_policy.score_thresholds.items():
                        if cat not in (policy.score_thresholds or {}):
                            if policy.score_thresholds is None:
                                policy.score_thresholds = {}
                            policy.score_thresholds[cat] = threshold
                # Similar merging for retries, timeouts, etc.
        
        # Create checkpoint store based on CLI flag
        def make_checkpoint_store(kind: str, root: str = "out"):
            """Factory function for checkpoint stores."""
            if kind == "sqlite":
                from src.orchestrator.checkpoint_sqlite import SQLiteCheckpointStore
                return SQLiteCheckpointStore(db_path=f"{root}/checkpoints.db")
            else:  # fs
                from src.orchestrator.checkpoint_fs import FileCheckpointStore
                return FileCheckpointStore(root=f"{root}/checkpoints")
        
        checkpoint_store = make_checkpoint_store(args.checkpoint_store, root="out")
        
        # Create orchestrator
        if args.parallel:
            orch = OrchestratorParallel(
                agent_factory=agent_factory,
                advisor_factory=advisor_factory,
                max_workers=args.max_workers,
                score_thresholds=score_thresholds,
                post_step_hooks=post_hooks,
            )
        else:
            orch = Orchestrator(
                agent_factory=agent_factory,
                advisor_factory=advisor_factory,
                checkpoint_store=checkpoint_store,
                post_step_hooks=post_hooks,
            )
            # Apply policy thresholds for sequential orchestrator
            orch.policy = policy
            
            # Load budget from policy if present
            if policy and policy.budget:
                from src.orchestrator.budget import Budget
                budget_data = policy.budget
                orch.budget = Budget(
                    max_runtime_sec=budget_data.get("max_runtime_sec"),
                    max_stages=budget_data.get("max_stages"),
                    max_artifacts_bytes=budget_data.get("max_artifacts_bytes"),
                )
        
        # Apply cache setting from CLI
        orch.use_cache = not args.no_cache
        
        # Resume from checkpoint if requested
        if args.resume_run_id:
            # Use the same checkpoint store as orchestrator
            store = orch.checkpoints if hasattr(orch, "checkpoints") else checkpoint_store
            if store is None:
                from src.orchestrator.checkpoint_fs import FileCheckpointStore
                store = FileCheckpointStore()
            
            last_key = store.find_last_key(args.resume_run_id)
            if last_key:
                checkpoint = store.load(last_key)
                if checkpoint:
                    orch.memory.update(checkpoint.memory_snapshot)
                    orch.run_id = args.resume_run_id
                    print(f"Resumed from checkpoint: {last_key}", file=sys.stderr)
                else:
                    print(f"Warning: No checkpoint found for run_id={args.resume_run_id}", file=sys.stderr)
            else:
                print(f"Warning: No checkpoint found for run_id={args.resume_run_id}", file=sys.stderr)

        # Seed memory from CLI overrides
        if args.mem:
            try:
                memory_overrides = parse_kv_pairs(args.mem)
                for k, v in memory_overrides.items():
                    orch.memory.set(k, v)
            except ValueError as e:
                print(f"Error parsing --mem: {e}", file=sys.stderr)
                sys.exit(1)

        # Run pipeline
        if args.parallel:
            result = orch.run_waves(steps)
        else:
            result = orch.run(steps)

        # Fail-fast check
        if args.fail_fast:
            for h in result["history"]:
                if not h.get("approved", False):
                    print(
                        f"FAIL-FAST: Stage '{h['stage']}' failed "
                        f"(score={h.get('score', 0):.2f}). "
                        "Run again with --output json for details or inspect "
                        f"out/<run_id>/ if --save-artifacts was used.",
                        file=sys.stderr,
                    )
                    sys.exit(1)

        # Save artifacts if requested
        artifacts_saved = False
        if args.save_artifacts:
            count = persist_artifacts(result, out_dir="out")
            run_dir = Path("out") / result.get("run_id", "unknown")
            print(
                f"\n[INFO] Saved {count} artifacts to: {run_dir}", file=sys.stderr
            )
            artifacts_saved = True

        # Output result
        if args.output == "human":
            report = build_markdown_report(
                result,
                artifacts_saved=artifacts_saved,
                top_suggestions=args.top_suggestions,
            )
            print(report)
        else:
            print(json.dumps(result, indent=2, default=str))

    except PipelineValidationError as e:
        print(f"Pipeline validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Pipeline file not found: {args.pipeline}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def clean_command() -> None:
    """Clean artifacts command entry point."""
    from scripts.clean_artifacts import main as clean_main
    sys.exit(clean_main())


if __name__ == "__main__":
    # Check if running as 'clean' command
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        sys.argv = sys.argv[1:]  # Remove 'clean' from args
        clean_command()
    else:
        main()

