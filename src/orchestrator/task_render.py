"""Task template rendering with Jinja2 support."""

from __future__ import annotations

from typing import Any, Dict

try:
    from jinja2 import Environment, StrictUndefined

    _env = Environment(undefined=StrictUndefined, autoescape=False)
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


def render_task(template: str, memory: Dict[str, Any]) -> str:
    """
    Render task template with memory values.

    Uses Jinja2 if available and template contains Jinja2 syntax ({{ }}),
    otherwise falls back to simple {key} replacement.

    Args:
        template: Task template string
        memory: Memory dictionary for template variables

    Returns:
        Rendered task string
    """
    # Check if template uses Jinja2 syntax
    uses_jinja2 = "{{" in template or "{%" in template

    if JINJA2_AVAILABLE and uses_jinja2:
        try:
            return _env.from_string(template).render(**memory)
        except Exception:
            # Fallback to simple replacement if Jinja2 fails
            pass

    # Simple {key} replacement fallback
    result = template
    for k, v in memory.items():
        token = "{" + k + "}"
        if token in result:
            result = result.replace(token, str(v))
    return result
