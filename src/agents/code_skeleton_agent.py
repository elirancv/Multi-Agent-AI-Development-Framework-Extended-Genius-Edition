"""Agent that generates static HTML/CSS code skeletons."""

from __future__ import annotations

from typing import Any, Dict

from src.core.base import BaseFunctionalAgent
from src.core.types import AgentMetadata, AgentOutput, Artifact

SIMPLE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <link rel="stylesheet" href="styles.css"/>
</head>
<body>
  <header><h1>{title}</h1><nav><a>Home</a> · <a>Products</a> · <a>Contact</a></nav></header>
  <main><section class="grid">{grid}</section></main>
  <footer>© {year} {brand}</footer>
</body>
</html>
"""

SIMPLE_CSS = """*{box-sizing:border-box}body{font-family:system-ui;margin:0;padding:0}
header,footer{padding:16px;border-bottom:1px solid #eee}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;padding:16px}
.card{border:1px solid #eee;border-radius:12px;padding:12px}
.card img{max-width:100%;border-radius:8px}
"""


class CodeSkeletonAgent(BaseFunctionalAgent):
    """Generates static HTML/CSS code skeletons."""

    name = "CodeSkeletonAgent"
    min_advisor_score = 0.90

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """Generate static HTML/CSS skeleton based on context."""
        title = (context.get("site_title") or "Store").strip()
        brand = (context.get("brand") or "Brand").strip()
        products = (context.get("products") or ["Sample #1", "Sample #2"])[0:6]
        year = context.get("year") or 2025

        grid = "\n".join(
            [
                f'<article class="card"><img alt="" src="https://placehold.co/400x300"/><h3>{p}</h3><p>$0.00</p></article>'
                for p in products
            ]
        )
        html = SIMPLE_HTML.format(title=title, brand=brand, year=year, grid=grid)

        artifacts = [
            Artifact(
                name="index.html",
                type="text",
                content=html,
                description="Static HTML skeleton",
            ),
            Artifact(
                name="styles.css",
                type="text",
                content=SIMPLE_CSS,
                description="Minimal CSS",
            ),
        ]

        meta = AgentMetadata(
            agent_name=self.name,
            stage=context.get("stage", "codegen"),
            input_summary=task[:200],
        )

        return AgentOutput(
            content="Generated static code skeleton.", artifacts=artifacts, metadata=meta
        )
