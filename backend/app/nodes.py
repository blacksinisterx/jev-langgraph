import time

from .providers.base import Provider
from .questions import QUESTIONS
from .schemas import ChoiceAnswer
from .state import MAX_REASONING_STEPS, MAX_RETRIES, MAX_TOTAL_STEPS, AgentState, Step


def _record(state: AgentState, node: str, detail: str, failed: bool = False, decision: dict | None = None) -> None:
    state["steps"].append(Step(node=node, detail=detail, failed=failed, decision=decision))


def make_decide_node(provider: Provider):
    def decide(state: AgentState) -> AgentState:
        if len(state["steps"]) >= MAX_TOTAL_STEPS:
            state["next_action"] = "escalate"
            _record(state, "decide", "forced escalate: max step budget reached", decision=None)
            return state

        jev_state = {
            "query": state["query"],
            "steps": [{"node": s["node"], "detail": s["detail"], "failed": s["failed"]} for s in state["steps"]],
            "retry_count": state["retry_count"],
            "reasoning_steps": state["reasoning_steps"],
            "search_done": state["search_done"],
            "tool_done": state["tool_done"],
        }
        start = time.perf_counter()
        answers = provider.evaluate(jev_state, QUESTIONS)
        latency_ms = (time.perf_counter() - start) * 1000
        answer = answers.get("next_action")
        choice = answer.choice if isinstance(answer, ChoiceAnswer) else "escalate"

        decision = {
            "choice": choice,
            "confidence": answer.confidence if isinstance(answer, ChoiceAnswer) else 0.0,
            "probabilities": answer.probabilities if isinstance(answer, ChoiceAnswer) else {},
            "latency_ms": round(latency_ms, 4),
        }
        state["next_action"] = choice
        if choice == "continue":
            state["reasoning_steps"] += 1
        _record(state, "decide", f"Jev chose '{choice}'", decision=decision)
        return state
    return decide


def search_node(state: AgentState) -> AgentState:
    from .tools import search
    result, failed = search(state["query"], state["search_attempts"])
    state["search_attempts"] += 1
    if not failed:
        state["search_done"] = True
    _record(state, "search", result, failed=failed)
    return state


def use_tool_node(state: AgentState) -> AgentState:
    from .tools import calculate
    result, failed = calculate(state["query"])
    if not failed:
        state["tool_done"] = True
    _record(state, "use_tool", result, failed=failed)
    return state


def retry_node(state: AgentState) -> AgentState:
    state["retry_count"] += 1
    # steps[-1] here is always the 'decide' step that just chose "retry" --
    # the actual failed action is the most recent step before that with failed=True.
    failed_step = next((s["node"] for s in reversed(state["steps"]) if s["failed"]), "unknown")
    _record(state, "retry", f"retrying after failed '{failed_step}' (attempt {state['retry_count']}/{MAX_RETRIES})")
    return state


def finish_node(state: AgentState) -> AgentState:
    parts = [s["detail"] for s in state["steps"] if s["node"] in ("search", "use_tool") and not s["failed"]]
    answer = "; ".join(parts) if parts else "No external information was needed to answer this."
    state["final_answer"] = answer
    _record(state, "finish", answer)
    return state


def escalate_node(state: AgentState) -> AgentState:
    if state["retry_count"] >= MAX_RETRIES:
        reason = f"gave up after {state['retry_count']} failed retries"
    elif state["reasoning_steps"] >= MAX_REASONING_STEPS:
        reason = "query is ambiguous or subjective -- no clear search/tool action resolves it"
    elif len(state["steps"]) >= MAX_TOTAL_STEPS:
        reason = "exceeded the maximum step budget without reaching an answer"
    else:
        reason = "agent could not determine how to proceed"
    state["escalation_reason"] = reason
    _record(state, "escalate", reason)
    return state


def route_from_decide(state: AgentState) -> str:
    return state["next_action"] or "escalate"
