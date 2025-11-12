# Parallel Execution Guide

## Overview

The system supports two execution modes:

1. **Sequential** (`Orchestrator`) - Executes steps one by one
2. **Parallel** (`OrchestratorParallel`) - Executes steps in dependency waves

## Parallel Execution

### How It Works

The parallel orchestrator:
- Groups steps into **waves** based on dependencies
- Executes all steps in a wave **in parallel**
- Waits for wave completion before starting next wave
- Uses thread-safe `SharedMemory` for concurrent access

### Example

```python
from src.orchestrator.runner_parallel import OrchestratorParallel
from src.orchestrator.factory import agent_factory, advisor_factory
from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict

# Load pipeline
loader = YAMLPipelineLoaderStrict()
steps, score_thresholds = loader.load("pipeline/with_codegen.yaml")

# Create parallel orchestrator
orch = OrchestratorParallel(
    agent_factory=agent_factory,
    advisor_factory=advisor_factory,
    max_workers=4,  # Parallel workers per wave
    score_thresholds=score_thresholds,
)

# Run in waves
result = orch.run_waves(steps)
```

### Wave Execution Example

For pipeline:
```
A (no deps)
B (depends on A)
C (depends on A)
D (depends on B, C)
```

Execution:
- **Wave 1:** A runs
- **Wave 2:** B and C run in parallel
- **Wave 3:** D runs

## CLI Usage

```bash
# Sequential execution (default)
python cli.py --pipeline pipeline/example.yaml

# Parallel execution
python cli.py --pipeline pipeline/with_codegen.yaml --parallel --max-workers 4

# Parallel with memory overrides
python cli.py --pipeline pipeline/with_codegen.yaml --parallel --mem product_idea='"Test"'
```

## Benefits

- **Faster execution** - Independent steps run simultaneously
- **Dependency-aware** - Maintains correct execution order
- **Thread-safe** - SharedMemory handles concurrent access
- **Policy support** - Category-based thresholds work in parallel mode

## When to Use Parallel

✅ **Use parallel when:**
- You have independent steps that can run simultaneously
- You want faster execution
- Steps don't modify shared state in conflicting ways

❌ **Use sequential when:**
- Steps have complex interdependencies
- You need strict ordering
- Debugging is easier with sequential execution

## Performance

Typical speedup:
- 2 independent steps: ~2x faster
- 4 independent steps: ~3-4x faster (limited by max_workers)
- Dependent steps: Same speed as sequential (must wait)

## Thread Safety

- `SharedMemory` uses `RLock` for thread-safe access
- Each step gets a deep copy of memory context
- Checkpoints are saved per step (not per wave)

