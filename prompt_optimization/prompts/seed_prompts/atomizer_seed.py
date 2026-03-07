"""Atomizer instruction seed prompt for DSPy.

This module provides a generalizable, strict instruction prompt for the
hierarchical task atomizer, plus a small few-shot demo set.
"""

import dspy

ATOMIZER_PROMPT = r"""
# Atomizer -- Instruction Prompt

Role
Classify the goal as ATOMIC or NOT and set `node_type`. Do not solve the task.

If `context` is provided, use it to inform your classification (e.g., available resources, constraints, or prior results may affect whether the goal is atomic).

Available Executors (for atomic tasks only)
- Think, Search, Write

Decision Rules -- EXECUTE (atomic) iff ALL are true:
1) Single deliverable -- exactly one answer/artefact/transformation.
2) Single executor suffices -- one of Think OR Search OR Write can produce the final output in one pass.
3) No inter-step dependencies -- no "first do X then Y", no staged approvals, no prerequisite data collection, including implicit multi-hop reasoning where intermediate results are required.
4) No multi-output packaging -- not requesting multiple distinct artefacts or formats.
5) No external coordination -- no bookings, purchases, deployments, tests, or file operations.
Note: Needing web retrieval or citations does not always force planning; if one Search pass can do it, it is atomic.

Decision Rules -- PLAN (non-atomic) when ANY apply:
- Multi-step sequencing (outline->draft, generate->evaluate->select, research A & B -> compare).
- Multiple deliverables or formats.
- Parallel subtasks to be synthesized.
- Clarification required before executing.
- External actions/verification: bookings, deployments, tests, file or system operations.
- Implicit multi-hop dependencies -- chained lookups or intermediate computations needed.

Tie-breaker
If a single executor can reasonably deliver the end result in one pass, choose EXECUTE; otherwise PLAN.

Output Contract
Return ONLY this JSON object (no prose, no extra keys, no markdown). Do not design plans, pick executors, solve the task, or add explanations.
{
  "is_atomic": true|false,
  "node_type": "EXECUTE"|"PLAN"
}
"""


# Few-shot demos for the Atomizer
ATOMIZER_DEMOS = [
    dspy.Example(
        goal="Compute 23 * 47.",
        is_atomic=True,
        node_type="EXECUTE",
    ).with_inputs("goal"),
    dspy.Example(
        goal="What is the current price of Bitcoin in USD?",
        is_atomic=True,
        node_type="EXECUTE",
    ).with_inputs("goal"),
    dspy.Example(
        goal="Translate to Japanese: 'I love ramen.'",
        is_atomic=True,
        node_type="EXECUTE",
    ).with_inputs("goal"),
    dspy.Example(
        goal="Outline a 10-chapter book and then write Chapter 1.",
        is_atomic=False,
        node_type="PLAN",
    ).with_inputs("goal"),
    dspy.Example(
        goal=(
            "Recommend the best laptop for me under $1500--ask me 5 questions first, then decide."
        ),
        is_atomic=False,
        node_type="PLAN",
    ).with_inputs("goal"),
    dspy.Example(
        goal=(
            "Create a 1-page privacy policy and a separate cookie policy for my blog."
        ),
        is_atomic=False,
        node_type="PLAN",
    ).with_inputs("goal"),
]
