"""OpenTelemetry integration for observability."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, Optional

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    import logging
    import warnings

    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    logging = None
    warnings = None

_tracer: Optional[Any] = None


def init_otel(
    service_name: str = "multi-agent",
    endpoint: str = "http://localhost:4318/v1/traces",
    fallback_to_console: bool = True,
) -> None:
    """
    Initialize OpenTelemetry tracing.

    Args:
        service_name: Service name for traces
        endpoint: OTLP HTTP endpoint URL
        fallback_to_console: If True, fall back to console exporter if OTLP fails
    """
    if not OPENTELEMETRY_AVAILABLE:
        return

    try:
        # Suppress warnings and connection errors
        if warnings:
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", message=".*connection.*", category=Warning)
        
        if logging:
            # Suppress urllib3/requests connection errors
            urllib3_logger = logging.getLogger("urllib3")
            urllib3_logger.setLevel(logging.CRITICAL)
            urllib3_logger.disabled = True
            requests_logger = logging.getLogger("requests")
            requests_logger.setLevel(logging.CRITICAL)
            requests_logger.disabled = True
            otlp_logger = logging.getLogger("opentelemetry.exporter.otlp")
            otlp_logger.setLevel(logging.CRITICAL)
            otlp_logger.disabled = True
            # Suppress OpenTelemetry SDK internal errors
            otel_logger = logging.getLogger("opentelemetry.sdk")
            otel_logger.setLevel(logging.CRITICAL)
            otel_logger.disabled = True
        
        tp = TracerProvider()
        
        # Try OTLP exporter first, but catch connection errors silently
        try:
            otlp_exporter = OTLPSpanExporter(endpoint)
            # Use BatchSpanProcessor with error suppression
            processor = BatchSpanProcessor(otlp_exporter)
            tp.add_span_processor(processor)
        except Exception:
            # If OTLP fails, fall back to console or no-op
            if fallback_to_console:
                try:
                    console_exporter = ConsoleSpanExporter()
                    tp.add_span_processor(BatchSpanProcessor(console_exporter))
                except Exception:
                    # If console also fails, use no-op (no processor)
                    pass
            # Otherwise, use no-op (no processor)
        
        trace.set_tracer_provider(tp)
        global _tracer
        _tracer = trace.get_tracer(service_name)
    except Exception:
        # Fail silently if OTel setup fails completely
        pass


@contextmanager
def span(name: str, attrs: Optional[Dict[str, Any]] = None):
    """
    Create a tracing span context manager.

    Args:
        name: Span name
        attrs: Optional span attributes

    Yields:
        Span object (or None if OTel not available)
    """
    if _tracer is None:
        yield None
        return

    try:
        with _tracer.start_as_current_span(name) as s:
            if attrs:
                for k, v in attrs.items():
                    try:
                        s.set_attribute(k, str(v))
                    except Exception:
                        # Ignore attribute setting errors
                        pass
            yield s
    except Exception:
        # Fail silently if span creation fails
        yield None

