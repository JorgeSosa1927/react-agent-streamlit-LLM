from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from .state import MASState
from .agents import (
    router_agent,
    research_agent,
    theory_agent,
    coding_agent,
    final_formatter,
)


def build_mas_graph():
    builder = StateGraph(MASState)

    builder.add_node("router", router_agent)
    builder.add_node("research", research_agent)
    builder.add_node("theory", theory_agent)
    builder.add_node("coding", coding_agent)
    builder.add_node("final", final_formatter)

    builder.add_edge(START, "router")

    def route_decision(state: MASState) -> str:
        qtype = state.get("query_type")
        if qtype == "research":
            return "research"
        elif qtype == "theory":
            return "theory"
        elif qtype == "coding":
            return "coding"
        else:
            return "coding"

    builder.add_conditional_edges(
        "router",
        route_decision,
        {"research": "research", "theory": "theory", "coding": "coding"},
    )

    builder.add_edge("research", "final")
    builder.add_edge("theory", "final")
    builder.add_edge("coding", "final")
    builder.add_edge("final", END)

    return builder.compile()


mas_graph = build_mas_graph()


if __name__ == "__main__":
    example_state: MASState = {
        "user_query": "Give me a summary of recent research on quantum computing",
        "agents_visited": [],
        "tools_used": [],
        "memory": [],
    }

    result = mas_graph.invoke(example_state)
    print("=== FINAL ANSWER ===")
    print(result.get("final_answer"))
    print("\nAgents visited:", result.get("agents_visited"))
    print("Tools used:", result.get("tools_used"))

