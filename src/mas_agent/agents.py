from __future__ import annotations

from typing import Dict, Any

from .state import MASState
from .tools import run_research_assistant


def router_agent(state: MASState) -> MASState:
    """Router súper simple basado en palabras clave."""
    query = state.get("user_query", "") or ""
    q = query.lower()

    if any(w in q for w in ["paper", "literature", "research", "study"]):
        query_type = "research"
    elif any(w in q for w in ["theory", "concept", "explain", "qué es", "que es"]):
        query_type = "theory"
    elif any(w in q for w in ["code", "python", "bug", "error", "implement"]):
        query_type = "coding"
    else:
        query_type = "planning"

    state["query_type"] = query_type
    state.setdefault("agents_visited", []).append("RouterAgent")
    return state


def research_agent(state: MASState) -> MASState:
    query = state["user_query"]
    memory = state.get("memory", [])

    result: Dict[str, Any] = run_research_assistant(query=query, memory=memory)

    state["research_result"] = result
    state["draft_answer"] = result.get("formatted_report", "No report produced.")
    state.setdefault("agents_visited", []).append("ResearchAgent")
    state.setdefault("tools_used", []).append("run_research_assistant")

    memory.append(
        {"query": query, "answer": state["draft_answer"], "type": "research"}
    )
    state["memory"] = memory

    return state


def theory_agent(state: MASState) -> MASState:
    query = state["user_query"]
    answer = (
        "This is a THEORY agent placeholder. It should explain theoretical concepts "
        f"related to your query: '{query}'.\n\n"
        "Later we can plug a real LLM here."
    )

    state["draft_answer"] = answer
    state.setdefault("agents_visited", []).append("TheoryAgent")

    memory = state.get("memory", [])
    memory.append({"query": query, "answer": answer, "type": "theory"})
    state["memory"] = memory
    return state


def coding_agent(state: MASState) -> MASState:
    query = state["user_query"]
    answer = (
        "This is a CODING/PLANNING agent placeholder.\n\n"
        f"It should help you with code or study planning related to: '{query}'."
    )

    state["draft_answer"] = answer
    state.setdefault("agents_visited", []).append("CodingAgent")

    memory = state.get("memory", [])
    memory.append({"query": query, "answer": answer, "type": "coding"})
    state["memory"] = memory
    return state


def final_formatter(state: MASState) -> MASState:
    draft = state.get("draft_answer") or "No draft answer produced."
    state["final_answer"] = draft
    state.setdefault("agents_visited", []).append("FinalFormatter")
    return state

