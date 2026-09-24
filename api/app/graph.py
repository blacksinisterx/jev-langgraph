from langgraph.graph import END, StateGraph

from .nodes import escalate_node, finish_node, make_decide_node, retry_node, route_from_decide, search_node, use_tool_node
from .providers.base import Provider
from .state import AgentState

NODE_NAMES = ["decide", "search", "use_tool", "retry", "finish", "escalate"]
STATIC_EDGES = [
    ("decide", "search"), ("decide", "use_tool"), ("decide", "retry"),
    ("decide", "finish"), ("decide", "escalate"), ("decide", "decide"),
    ("search", "decide"), ("use_tool", "decide"), ("retry", "decide"),
]


def build_graph(provider: Provider):
    graph = StateGraph(AgentState)
    graph.add_node("decide", make_decide_node(provider))
    graph.add_node("search", search_node)
    graph.add_node("use_tool", use_tool_node)
    graph.add_node("retry", retry_node)
    graph.add_node("finish", finish_node)
    graph.add_node("escalate", escalate_node)

    graph.set_entry_point("decide")
    graph.add_conditional_edges("decide", route_from_decide, {
        "continue": "decide",
        "search": "search",
        "use_tool": "use_tool",
        "retry": "retry",
        "finish": "finish",
        "escalate": "escalate",
    })
    graph.add_edge("search", "decide")
    graph.add_edge("use_tool", "decide")
    graph.add_edge("retry", "decide")
    graph.add_edge("finish", END)
    graph.add_edge("escalate", END)

    return graph.compile()
