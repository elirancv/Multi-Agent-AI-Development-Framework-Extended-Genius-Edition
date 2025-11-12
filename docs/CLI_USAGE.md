# CLI Usage Guide

## Basic Usage

```bash
# Run pipeline from YAML file
python cli.py --pipeline pipeline/example.yaml

# With memory overrides
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"eBay template"' stage='"requirements"'

# With fail-fast (stop on first rejection)
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"Test"' --fail-fast

# JSON output format
python cli.py --pipeline pipeline/example.yaml --output json
```

## Memory Overrides

Use `--mem` to override memory values:

```bash
# Simple string value
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"My Product"'

# Multiple values
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"Product"' stage='"requirements"'

# JSON values (use quotes)
python cli.py --pipeline pipeline/example.yaml --mem config='{"debug": true, "timeout": 30}'
```

## Advanced Pipeline

Use `pipeline/advanced.yaml` for pipelines with dependencies and policy:

```bash
python cli.py --pipeline pipeline/advanced.yaml --mem product_idea='"Advanced Product"'
```

## Examples

### Example 1: Basic Run
```bash
python cli.py --pipeline pipeline/example.yaml
```

### Example 2: With Custom Product Idea
```bash
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"A mobile app for task management"'
```

### Example 3: Fail-Fast Mode
```bash
python cli.py --pipeline pipeline/example.yaml --mem product_idea='"Test"' --fail-fast
```

### Example 4: JSON Output
```bash
python cli.py --pipeline pipeline/example.yaml --output json > result.json
```

## Exit Codes

- `0` - Success (all stages approved)
- `1` - Failure (validation error, file not found, or fail-fast triggered)

## Help

```bash
python cli.py --help
```

