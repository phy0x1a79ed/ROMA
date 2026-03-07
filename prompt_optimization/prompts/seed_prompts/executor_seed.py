"""Generic executor instruction seed prompt for DSPy.

This module provides a general-purpose instruction prompt and demos for the default
executor (used as fallback when task doesn't match specific task type mappings).
"""

import dspy

EXECUTOR_PROMPT = r"""
# Executor -- Instruction Prompt

Role
Execute the given goal and produce a complete result. You are a leaf-node executor in a task tree -- your goal has already been decomposed and scoped for you.

If `context` is provided (as XML), it contains execution context from parent tasks -- prior results, constraints, or data you should use. Parse it before starting.

Execution Approach
1. Parse the goal and any provided context to understand exactly what is required.
2. Determine if tools are needed or if reasoning alone suffices. You may have tools available (search, code execution, file I/O, etc.) -- use them when the goal requires external data or actions.
3. Execute with targeted tool calls or direct reasoning.
4. If a tool call fails, adapt your approach rather than retrying the same call.
5. Synthesize your work into the `output` field, ensuring it fully addresses the goal.

Output Contract (strict)
- `output` (string): The complete result addressing the goal.
- `sources` (list[str]): Tools, APIs, or resources used. Empty list if pure reasoning.

Quality Standards
- Accuracy: Provide correct, verified information.
- Completeness: Address all aspects of the goal -- partial answers get rejected by the verifier.
- Clarity: Use structured formats (lists, tables) when they aid comprehension.
- Source transparency: List all external data sources in `sources`.
"""

EXECUTOR_DEMOS = [
    # Demo 1: Simple reasoning task (no tools)
    dspy.Example(
        goal="Explain the difference between microservices and monolithic architecture",
        output=(
            "Key differences between microservices and monolithic architecture:\n\n"
            "**Monolithic Architecture:**\n"
            "- Single, unified codebase for entire application\n"
            "- All components tightly coupled\n"
            "- Deployed as one unit\n"
            "- Scaling requires scaling entire application\n"
            "- Simpler to develop initially but harder to maintain at scale\n\n"
            "**Microservices Architecture:**\n"
            "- Application split into small, independent services\n"
            "- Each service handles specific business capability\n"
            "- Services communicate via APIs (HTTP, messaging)\n"
            "- Independent deployment and scaling per service\n"
            "- More complex initially but easier to scale and maintain\n\n"
            "**Trade-offs:**\n"
            "- Monolithic: Better for small teams, simple applications, rapid prototyping\n"
            "- Microservices: Better for large teams, complex domains, need for independent scaling"
        ),
        sources=[]
    ).with_inputs("goal"),

    # Demo 2: Calculation task
    dspy.Example(
        goal="Calculate compound interest for $10,000 at 5% annual rate over 10 years",
        output=(
            "Compound Interest Calculation:\n\n"
            "Principal (P): $10,000\n"
            "Annual Rate (r): 5% (0.05)\n"
            "Time (t): 10 years\n"
            "Compounding: Annual (n=1)\n\n"
            "Formula: A = P(1 + r/n)^(nt)\n"
            "A = 10,000 x (1 + 0.05/1)^(1x10)\n"
            "A = 10,000 x (1.05)^10\n"
            "A = 10,000 x 1.62889\n\n"
            "**Final Amount: $16,288.95**\n"
            "**Interest Earned: $6,288.95**"
        ),
        sources=[]
    ).with_inputs("goal"),

    # Demo 3: Comparison task
    dspy.Example(
        goal="Compare Python and JavaScript for backend development",
        output=(
            "Python vs JavaScript for Backend Development:\n\n"
            "**Python Advantages:**\n"
            "- Clean, readable syntax\n"
            "- Rich ecosystem for data science, ML, automation\n"
            "- Django/Flask for web development\n"
            "- Strong in scientific computing\n"
            "- Synchronous by default (simpler mental model)\n\n"
            "**JavaScript (Node.js) Advantages:**\n"
            "- Same language for frontend and backend\n"
            "- Excellent async/event-driven model\n"
            "- Large npm ecosystem\n"
            "- Fast execution (V8 engine)\n"
            "- JSON-native (web APIs)\n\n"
            "**Best Use Cases:**\n"
            "- Python: Data pipelines, ML services, scientific computing, automation\n"
            "- JavaScript: Real-time apps, microservices, full-stack JS teams, API gateways\n\n"
            "**Recommendation:**\n"
            "Choose Python for data-heavy work; JavaScript for real-time/full-stack scenarios"
        ),
        sources=[]
    ).with_inputs("goal"),

    # Demo 4: Problem-solving task
    dspy.Example(
        goal="How would you design a rate limiting system for an API?",
        output=(
            "Rate Limiting System Design:\n\n"
            "**1. Requirements:**\n"
            "- Limit requests per user/IP (e.g., 100 req/min)\n"
            "- Distribute across multiple servers\n"
            "- Low latency overhead (<5ms)\n"
            "- Handle burst traffic gracefully\n\n"
            "**2. Algorithm Choice:**\n"
            "Token Bucket (recommended):\n"
            "- Each user gets bucket with N tokens\n"
            "- Tokens refill at fixed rate (R/second)\n"
            "- Request consumes 1 token\n"
            "- Allows burst up to bucket size\n\n"
            "**3. Implementation:**\n"
            "Storage: Redis (distributed, fast)\n"
            "Key: user_id:api_key\n"
            "Value: { tokens: N, last_refill: timestamp }\n"
            "TTL: Set to prevent memory leak\n\n"
            "**4. Request Flow:**\n"
            "1. Extract user ID from request\n"
            "2. Get current token count from Redis\n"
            "3. Refill tokens based on time elapsed\n"
            "4. If tokens > 0: allow request, decrement tokens\n"
            "5. If tokens = 0: reject with 429 status\n\n"
            "**5. Edge Cases:**\n"
            "- Clock skew: Use Redis server time\n"
            "- Redis failure: Fallback to allow (fail open) or memory cache\n"
            "- Different limits per endpoint: Use separate buckets"
        ),
        sources=[]
    ).with_inputs("goal"),
]
