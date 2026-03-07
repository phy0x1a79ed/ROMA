"""
Resilience patterns for ROMA-DSPy agent architecture.

This module provides fault tolerance beyond error boundaries, focusing on:
- Task-level retry strategies with exponential backoff
- Module-level circuit breakers
- State recovery through checkpointing
- Compensation handlers for rollback scenarios
- Graceful degradation under failure conditions
"""

from .retry_policy import RetryPolicy, create_default_retry_policy
from .circuit_breaker import (
    CircuitBreaker,
    ModuleCircuitBreaker,
    module_circuit_breaker,
)
from .checkpoint_manager import CheckpointManager
from .decorators import (
    with_retry,
    with_circuit_breaker,
    with_module_resilience,
    measure_execution_time,
)
from .parse_retry import (
    ParseFailure,
    ParseRetryError,
    is_parse_error,
    extract_error_feedback,
    format_failed_attempts,
    MAX_PARSE_RETRIES,
)

__all__ = [
    "RetryPolicy",
    "create_default_retry_policy",
    "CircuitBreaker",
    "ModuleCircuitBreaker",
    "module_circuit_breaker",
    "CheckpointManager",
    "with_retry",
    "with_circuit_breaker",
    "with_module_resilience",
    "measure_execution_time",
    "ParseFailure",
    "ParseRetryError",
    "is_parse_error",
    "extract_error_feedback",
    "format_failed_attempts",
    "MAX_PARSE_RETRIES",
]
