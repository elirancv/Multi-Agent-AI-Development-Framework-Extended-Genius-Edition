"""Demo script for running the multi-agent pipeline."""

from src.orchestrator.runner import Orchestrator
from src.orchestrator.factory import agent_factory, advisor_factory
from src.orchestrator.yaml_loader import YAMLPipelineLoader


def main() -> None:
    """Run demo pipeline."""
    # Create orchestrator
    orch = Orchestrator(agent_factory=agent_factory, advisor_factory=advisor_factory)

    # Seed memory
    orch.memory.set("product_idea", "A static, responsive HTML/CSS template system for eBay stores")
    orch.memory.set("stage", "requirements")

    # Load pipeline from YAML
    loader = YAMLPipelineLoader()
    steps, policy = loader.load_from_file("pipeline/example.yaml")

    # Apply policy
    orch.policy = policy

    # Run pipeline
    result = orch.run(steps)

    # Print results
    print("=" * 60)
    print("Pipeline Execution Results")
    print("=" * 60)
    print(f"Run ID: {result['run_id']}")
    print("\nHistory:")
    for hist in result["history"]:
        status = "✓ APPROVED" if hist["approved"] else "✗ REJECTED"
        print(
            f"  [{hist['stage']}] {hist['agent']} → {hist['advisor']}: "
            f"{status} (score: {hist['score']:.2f})"
        )

    print("\n" + "=" * 60)
    print("Memory Contents:")
    print("=" * 60)
    memory = result["memory"]
    for key in sorted(memory.keys()):
        value = memory[key]
        if isinstance(value, str) and len(value) > 200:
            print(f"{key}: {value[:200]}...")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()

