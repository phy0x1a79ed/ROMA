"""
NodeType enumeration for ROMA v2.0

Defines whether a task node should be decomposed (PLAN) or executed atomically (EXECUTE).
This is the core decision made by the Atomizer.
"""

from enum import Enum
from typing import Literal


class NodeType(str, Enum):
    """
    Type of processing a node should perform.

    This is determined by the Atomizer based on task complexity:
    - PLAN: Task needs decomposition into subtasks
    - EXECUTE: Task is atomic and can be executed directly
    """

    PLAN = "PLAN"  # Decompose task into subtasks
    EXECUTE = "EXECUTE"  # Execute task atomically

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _missing_(cls, value):
        """Handle common LLM variations like 'NodeType.EXECUTE', quoted values, etc."""
        if isinstance(value, str):
            cleaned = value.strip().strip("'\"")
            # Strip class prefix: "NodeType.EXECUTE" → "EXECUTE"
            dot = cleaned.rfind(".")
            if dot != -1:
                cleaned = cleaned[dot + 1:]
            cleaned = cleaned.upper()
            for member in cls:
                if member.value == cleaned:
                    return member
        return None

    @classmethod
    def from_string(cls, value: str) -> "NodeType":
        """
        Convert string to NodeType, handling common LLM variations.

        Args:
            value: String representation of node type

        Returns:
            NodeType enum value

        Raises:
            ValueError: If value is not a valid node type
        """
        try:
            return cls(value)
        except ValueError:
            valid_types = [t.value for t in cls]
            raise ValueError(f"Invalid node type '{value}'. Valid types: {valid_types}")

    @property
    def is_plan(self) -> bool:
        """Check if this is a PLAN node type."""
        return self == NodeType.PLAN

    @property
    def is_execute(self) -> bool:
        """Check if this is an EXECUTE node type."""
        return self == NodeType.EXECUTE


# Type hints for use in other modules
NodeTypeLiteral = Literal["PLAN", "EXECUTE"]
