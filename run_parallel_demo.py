"""Demo script for running parallel pipeline."""

from src.orchestrator.factory import advisor_factory, agent_factory
from src.orchestrator.runner_parallel import OrchestratorParallel
from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict


def main() -> None:
    """Run parallel pipeline demo."""
    # Load pipeline with strict validation
    loader = YAMLPipelineLoaderStrict()
    steps, score_thresholds = loader.load("pipeline/with_codegen.yaml")

    # Create parallel orchestrator
    orch = OrchestratorParallel(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
        max_workers=4,
        score_thresholds=score_thresholds,
    )

    # Seed memory
    orch.memory.set("product_idea", "A static, responsive HTML/CSS template system for eBay stores")
    orch.memory.set("site_title", "eBay Store Template")
    orch.memory.set("brand", "My Store")
    orch.memory.set("products", ["Product 1", "Product 2", "Product 3"])

    # Run pipeline in waves
    result = orch.run_waves(steps)

    # Print results
    print("=" * 60)
    print("Parallel Pipeline Execution Results")
    print("=" * 60)
    print(f"Run ID: {result['run_id']}")
    print("\nStage History (executed in waves):")
    for hist in result["history"]:
        status = "✓ APPROVED" if hist["approved"] else "✗ REJECTED"
        print(
            f"  [{hist['stage']}] {hist['agent']} → {hist['advisor']}: "
            f"{status} (score: {hist['score']:.2f}, category: {hist['category']})"
        )

    print("\n" + "=" * 60)
    print("Generated Artifacts:")
    print("=" * 60)
    memory = result["memory"]
    for key in sorted(memory.keys()):
        if key.endswith(".artifacts"):
            artifacts = memory[key]
            print(f"\n{key}:")
            for art in artifacts:
                print(f"  - {art['name']} ({art['type']})")


if __name__ == "__main__":
    main()
