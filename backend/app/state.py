from typing import TypedDict


class Step(TypedDict):
    node: str
    detail: str
    failed: bool
    decision: dict | None  # {"choice", "confidence", "probabilities"} when this step was a `decide` call


class AgentState(TypedDict):
    query: str
    steps: list[Step]
    search_done: bool
    tool_done: bool
    retry_count: int
    reasoning_steps: int
    search_attempts: int
    next_action: str | None
    final_answer: str | None
    escalation_reason: str | None


MAX_RETRIES = 2
MAX_REASONING_STEPS = 3
MAX_TOTAL_STEPS = 10


def initial_state(query: str) -> AgentState:
    return AgentState(
        query=query, steps=[], search_done=False, tool_done=False, retry_count=0,
        reasoning_steps=0, search_attempts=0, next_action=None, final_answer=None,
        escalation_reason=None,
    )
