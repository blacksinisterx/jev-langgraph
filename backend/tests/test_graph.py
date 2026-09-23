from app.graph import build_graph
from app.providers.mock import MockProvider
from app.state import MAX_TOTAL_STEPS, initial_state

provider = MockProvider()


def _run(query: str) -> dict:
    graph = build_graph(provider)
    return graph.invoke(initial_state(query))


def test_pure_calculation_uses_tool_and_finishes():
    result = _run("What is 47 * 68?")
    nodes = [s["node"] for s in result["steps"]]
    assert "use_tool" in nodes
    assert "search" not in nodes
    assert result["final_answer"] is not None
    assert "3196" in result["final_answer"]


def test_pure_search_finishes_with_answer():
    result = _run("What is the latest stable version of Python?")
    nodes = [s["node"] for s in result["steps"]]
    assert "search" in nodes
    assert result["final_answer"] is not None


def test_search_and_tool_both_used():
    result = _run("What is the capital of France? Also calculate 128 + 256.")
    nodes = [s["node"] for s in result["steps"]]
    assert "search" in nodes
    assert "use_tool" in nodes
    assert result["final_answer"] is not None


def test_flaky_search_triggers_a_real_retry_then_succeeds():
    result = _run("Look up today's exchange rate and convert 100 USD to EUR.")
    nodes = [s["node"] for s in result["steps"]]
    assert "retry" in nodes
    assert result["steps"][1]["failed"] is True  # the first search attempt
    assert result["final_answer"] is not None
    retry_step = next(s for s in result["steps"] if s["node"] == "retry")
    assert "search" in retry_step["detail"]  # names the action that actually failed, not 'decide'


def test_ambiguous_query_escalates_to_human():
    result = _run("Should I accept a job offer with lower pay but a team I like more?")
    assert result["final_answer"] is None
    assert result["escalation_reason"] is not None


def test_graph_always_terminates_within_step_budget():
    result = _run("asdkjfh qwoeiru random gibberish query")
    assert len(result["steps"]) <= MAX_TOTAL_STEPS + 1
    assert result["final_answer"] is not None or result["escalation_reason"] is not None
