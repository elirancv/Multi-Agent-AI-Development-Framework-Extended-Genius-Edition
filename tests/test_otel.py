"""Tests for OpenTelemetry integration."""

from src.orchestrator.otel import init_otel, span


def test_otel_init_no_error():
    """Test that OTel initialization doesn't crash when opentelemetry is not installed."""
    # Should not raise even if opentelemetry is not installed
    init_otel("test-service", "http://localhost:4318/v1/traces")


def test_span_context_manager():
    """Test that span context manager works even without OTel."""
    # Should not raise even if opentelemetry is not installed
    with span("test_span", {"key": "value"}):
        pass
