# Quick Architecture

## TL;DR

Policy-driven pipelines: **Agents create → Advisors/Council review → Quality Gate → Persist + Checkpoint → Next stage**. Everything is YAML-configured, observable, resumable, and cacheable.

---

## Lifecycle

1. **CLI loads YAML (+preset)** → steps, policy, DAG
2. **Render task** via Jinja2 from SharedMemory
3. **Run Agent** → `AgentOutput(content, artifacts, metadata)`
4. **Review** (Advisor/Council, weighted decision) → `AdvisorReview(score, approved)`
5. **Gate** (thresholds per category) → retry or proceed
6. **Persist** artifacts (+manifest) + checkpoint snapshot
7. **Parallel waves** (no deps) + eventlog + durations
8. **Resume / cache hits** (includes `agent_version`)

---

## Data Shapes

```python
AgentOutput(
    content: str,
    artifacts: list[Artifact],
    metadata: AgentMetadata
)

AdvisorReview(
    score: float,  # 0.0-1.0
    approved: bool,
    summary: str = "",
    suggestions: list[str] = [],
    critical_issues: list[str] = []
)
```

---

## Prove It Works (60s)

```bash
pip install playwright && playwright install chromium

python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' \
  --save-artifacts --output human
```

**Artifacts:** `index.html`, `README.md`, `lint_report.md`, `a11y_report.md`, `screenshot.png`, `MANIFEST.txt`, ZIP package.

---

## Resume / Cache

```bash
python cli.py --pipeline pipeline/production.yaml --resume-run-id <run_id>
```

**Cache invalidates when `agent_version` changes.**

---

## Parallel DAG

Waves per dependencies; independent stages run concurrently with `--parallel --max-workers N`.

---

## Extensibility

- **Presets** (`--preset`) - Pre-configured profiles
- **Plugin entry-points** - External Agents/Advisors
- **Gallery pipelines** - Including marketing-first

---

## What's Next (Recommended, 5 Short Steps)

### 1. Update Badges (if not updated)

```bash
cp .env.example .env  # Fill OWNER/REPO
./scripts/revalidate.sh
```

### 2. Production Demo Locally + Tests

```bash
pip install playwright && playwright install chromium
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' \
  --save-artifacts --output human
pytest tests/test_idea_to_zip_integration.py -q
```

### 3. Smoke/Validation Tests

```bash
python scripts/smoke_test.py --skip-slow --json
./scripts/revalidate.sh
```

### 4. Create Release with Assets (ZIP+Screenshot+Summary)

```bash
./scripts/create_release_with_assets.sh v1.0.0
# Or: .\scripts\create_release_with_assets.ps1 -Tag "v1.0.0"
```

### 5. Open Milestone v1.1 + Issues

```bash
./scripts/create_v1.1_issues.sh
```

---

📖 **Full details:** See [ARCHITECTURE.md](ARCHITECTURE.md) for deep-dive.
