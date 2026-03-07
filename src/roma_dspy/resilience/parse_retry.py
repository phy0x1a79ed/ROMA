"""Parse-retry mechanism: retries LLM calls with error feedback on output parsing failures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

MAX_PARSE_RETRIES = 2


@dataclass
class ParseFailure:
    """A single failed parse attempt."""

    raw_response: str
    error_message: str
    attempt: int


class ParseRetryError(Exception):
    """All parse retry attempts exhausted."""

    def __init__(self, failures: list[ParseFailure], original_error: Exception):
        self.failures = failures
        self.original_error = original_error
        last = failures[-1].error_message
        super().__init__(
            f"Output parsing failed after {len(failures)} attempts. Last error: {last}"
        )


def is_parse_error(error: Exception) -> bool:
    """Classify whether an error is a parse/validation error worth retrying with feedback."""
    if type(error).__name__ == "AdapterParseError":
        return True
    if isinstance(error, (ValueError, TypeError, AttributeError)):
        msg = str(error).lower()
        parse_keywords = [
            "missing",
            "field",
            "expected",
            "enum",
            "not a valid",
            "wrong type",
            "must be",
        ]
        return any(kw in msg for kw in parse_keywords)
    return False


def extract_error_feedback(error: Exception) -> tuple[str, str]:
    """Extract (raw_response, user_friendly_message) from an error."""
    raw = getattr(error, "lm_response", "") or ""
    msg = str(error)
    if "failed to parse" in msg.lower():
        lines = msg.split("\n")
        msg = lines[0] if lines else msg
    return (raw[:2000], msg[:500])


def format_failed_attempts(failures: list[ParseFailure]) -> str:
    """Format failures as XML for injection into LLM context."""
    parts = [
        "<failed_attempts>",
        "Your previous response(s) could not be parsed. Fix the errors below.",
    ]
    for f in failures:
        parts.append(f'<attempt number="{f.attempt + 1}">')
        if f.raw_response:
            parts.append(f"  <your_response>{f.raw_response[:1000]}</your_response>")
        parts.append(f"  <error>{f.error_message}</error>")
        parts.append("</attempt>")
    parts.append("</failed_attempts>")
    return "\n".join(parts)
