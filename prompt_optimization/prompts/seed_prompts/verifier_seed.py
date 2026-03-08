"""Verifier instruction seed prompt for DSPy.

This module provides a strict instruction prompt for the
verifier along with few-shot demos demonstrating verification patterns.
"""

import dspy

VERIFIER_PROMPT = r"""
# Verifier -- Instruction Prompt

Role
Validate that the candidate output fully satisfies the original goal. Provide actionable feedback when it does not.

If `context` is provided, use it as additional background -- but verify against the `goal`, not the context.

Output Contract (strict)
- `verdict` (bool): true if output satisfies goal, false otherwise
- `feedback` (string): Actionable explanation when false, brief confirmation when true

Verification Process
1. Extract ALL requirements from the goal -- explicit (stated directly), implicit (reasonably inferred, e.g. units), and format (list, table, JSON, etc.).
2. Check each requirement against the candidate output.
3. Evaluate correctness of factual claims where verifiable.
4. Verdict: ALL requirements must be met for TRUE. Missing any -> FALSE.

When FALSE -- feedback rules:
- Reference the goal: "The goal requires X, but output lacks X."
- Be specific: "Missing cost analysis" not "incomplete."
- Provide direction: "Add a table comparing X vs Y."
- Numbered list for multiple issues.
- Never be lenient on missing requirements.

When TRUE: Brief confirmation (1-2 sentences).

Do NOT accept partial completion, add requirements beyond the goal, approve factual errors, or focus on style unless the goal specifies it. Extra content beyond the goal is acceptable if all requirements are met.

Temporal Tolerance
For time-sensitive queries (current time, "right now", etc.), accept answers that were correct at the time of execution, even if the context timestamp has since advanced. A few seconds of drift between execution and verification is expected and acceptable.

Examples of GOOD feedback (when false):
"The goal requests (1) definition, (2) example, (3) use case. Output provides definition and example but omits use case. Add a use case section."

"The goal asks for comparison of A and B. Output only describes A. Add B and a direct comparison."

Examples of BAD feedback:
"Needs improvement." / "Good answer!" / "Missing something." (too vague -- say what specifically)
"""


# Few-shot demos for the Verifier
VERIFIER_DEMOS = [
    # 1) Complete and correct answer -> TRUE
    dspy.Example(
        goal="What is the capital of France?",
        candidate_output="The capital of France is Paris.",
        verdict=True,
        feedback="Output correctly and completely answers the goal."
    ).with_inputs("goal", "candidate_output"),

    # 2) Incomplete answer -> FALSE
    dspy.Example(
        goal="List the first 5 prime numbers.",
        candidate_output="The first 3 prime numbers are: 2, 3, 5",
        verdict=False,
        feedback="The goal requests 5 prime numbers, but the output only provides 3 (2, 3, 5). Missing: 7 and 11. Add the remaining two prime numbers to satisfy the goal."
    ).with_inputs("goal", "candidate_output"),

    # 3) Missing required element -> FALSE
    dspy.Example(
        goal="Convert 100 kilometers to miles and show the conversion formula.",
        candidate_output="100 kilometers equals approximately 62.14 miles.",
        verdict=False,
        feedback="The goal requires two elements: (1) the conversion result, and (2) the conversion formula. The output provides the result but omits the formula. Add the conversion formula (1 km = 0.621371 miles) to satisfy the goal."
    ).with_inputs("goal", "candidate_output"),

    # 4) Complete with all requirements -> TRUE
    dspy.Example(
        goal="Convert 100 kilometers to miles and show the conversion formula.",
        candidate_output="100 kilometers equals approximately 62.14 miles. Conversion formula: 1 km = 0.621371 miles, therefore 100 km x 0.621371 = 62.1371 miles.",
        verdict=True,
        feedback="Output provides both the conversion result and formula as required by the goal."
    ).with_inputs("goal", "candidate_output"),

    # 5) Wrong answer -> FALSE
    dspy.Example(
        goal="Is 15 a prime number?",
        candidate_output="Yes, 15 is a prime number.",
        verdict=False,
        feedback="The output is factually incorrect. 15 is not a prime number because it is divisible by 3 and 5 (15 = 3 x 5). A prime number must only be divisible by 1 and itself. Correct the answer to 'No, 15 is not a prime number' and explain why."
    ).with_inputs("goal", "candidate_output"),

    # 6) Missing comparison -> FALSE
    dspy.Example(
        goal="Compare the populations of Tokyo and New York City.",
        candidate_output="Tokyo has a population of approximately 14 million in the city proper and 37 million in the metro area.",
        verdict=False,
        feedback="The goal requires a comparison of Tokyo and New York City. The output only provides Tokyo's population data. Add New York City's population and a direct comparison (e.g., 'Tokyo metro (37M) is larger than NYC metro (20M)')."
    ).with_inputs("goal", "candidate_output"),

    # 7) Complete comparison -> TRUE
    dspy.Example(
        goal="Compare the populations of Tokyo and New York City.",
        candidate_output="Tokyo has approximately 14 million people in the city proper (37 million in metro area), while New York City has about 8.3 million (20 million in metro area). Tokyo's metropolitan area is significantly larger, nearly double that of New York City.",
        verdict=True,
        feedback="Output provides population data for both cities and includes a clear comparison as required."
    ).with_inputs("goal", "candidate_output"),

    # 8) Format mismatch -> FALSE
    dspy.Example(
        goal="List the benefits of exercise in a bulleted list.",
        candidate_output="Exercise improves cardiovascular health, strengthens muscles, enhances mood, aids weight management, and boosts energy levels.",
        verdict=False,
        feedback="The goal specifies a 'bulleted list' format, but the output is a paragraph. Reformat as a bulleted list."
    ).with_inputs("goal", "candidate_output"),

    # 9) Correct format -> TRUE
    dspy.Example(
        goal="List the benefits of exercise in a bulleted list.",
        candidate_output="- Improves cardiovascular health\n- Strengthens muscles\n- Enhances mood\n- Aids weight management\n- Boosts energy levels",
        verdict=True,
        feedback="Output correctly uses bulleted list format and provides relevant benefits as requested."
    ).with_inputs("goal", "candidate_output"),

    # 10) Missing multiple elements -> FALSE
    dspy.Example(
        goal="Explain what a prime number is, provide an example, and state its use in cryptography.",
        candidate_output="A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. For example, 7 is a prime number.",
        verdict=False,
        feedback="The goal requires three elements: (1) definition, (2) example, (3) cryptographic use. The output provides definition and example but omits the cryptographic use case. Add an explanation of how prime numbers are used in cryptography (e.g., in RSA encryption) to satisfy the goal."
    ).with_inputs("goal", "candidate_output"),

    # 11) All elements present -> TRUE
    dspy.Example(
        goal="Explain what a prime number is, provide an example, and state its use in cryptography.",
        candidate_output="A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. For example, 7 is a prime number because it is only divisible by 1 and 7. In cryptography, prime numbers are fundamental to RSA encryption, where the security relies on the difficulty of factoring large numbers into their prime factors.",
        verdict=True,
        feedback="Output addresses all three required elements: definition, example, and cryptographic use case."
    ).with_inputs("goal", "candidate_output"),
]
