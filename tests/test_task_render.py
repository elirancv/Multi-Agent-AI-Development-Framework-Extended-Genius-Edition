"""Test task template rendering."""

from src.orchestrator.task_render import render_task


def test_simple_replacement() -> None:
    """Test simple {key} replacement."""

    memory = {"product_idea": "Todo App", "stage": "requirements"}
    template = "Create PRD for: {product_idea}"
    result = render_task(template, memory)
    assert result == "Create PRD for: Todo App"


def test_jinja2_if_available() -> None:
    """Test Jinja2 rendering if available."""

    memory = {"product_idea": "Todo App", "requirements": {"review": {"score": 0.9}}}
    template = "Create PRD for: {{ product_idea }}. Last score: {{ requirements.review.score }}"
    result = render_task(template, memory)

    # Should render with Jinja2 if available, or fallback to simple replacement
    assert "Todo App" in result
    assert "0.9" in result or "N/A" in result


def test_multiple_replacements() -> None:
    """Test multiple variable replacements."""

    memory = {"product_idea": "App", "category": "mobile"}
    template = "Build {product_idea} for {category}"
    result = render_task(template, memory)
    assert "App" in result
    assert "mobile" in result

