from langgraph.graph import StateGraph
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.output_parsers import StrOutputParser

from typing import Dict, List
import json

from react_agent.tools import fetch_papers_openalex, fetch_author_stats
from react_agent.state import State, InputState
from react_agent.prompts import PLANNER_PROMPT, WRITER_PROMPT, FORMATTER_PROMPT
from react_agent.models import LiteraturePlan, LiteratureSummary
from react_agent.utils import load_chat_model
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_papers_with_retry(plan: LiteraturePlan):
    return fetch_papers_openalex(plan)


# Planner node
async def planner_node(state: State, runtime: Runtime) -> Dict:
    model = load_chat_model(runtime.context)
    system_prompt = PLANNER_PROMPT.strip()

    result = await model.ainvoke([
        {"role": "system", "content": system_prompt},
        *state.messages
    ])

    print("\nRAW LLM OUTPUT:\n", result.content)

    try:
        parsed = json.loads(result.content)
        print("Parsed JSON:", parsed)
        print("Expected by LiteraturePlan:", LiteraturePlan.model_fields.keys())

        plan = LiteraturePlan(**parsed)
        return {
            "plan": plan,
            "messages": state.messages
        }
    except Exception as e:
        print("Error parsing plan:", e)
        print("Received content:", result.content)
        raise ValueError(f"Planner failed to return valid JSON: {e}\nOutput: {result.content}")


# OpenAlex node: search for papers
async def openalex_node(state: State, runtime: Runtime) -> Dict:
    papers = fetch_papers_with_retry(state.plan)
    return {
        "papers": papers,
        "plan": state.plan,
        "messages": state.messages
    }


# Optional node: fetch author statistics
async def author_stats_node(state: State, runtime: Runtime) -> Dict:
    stats = fetch_author_stats(state.plan)
    return {
        "author_stats": stats,
        "plan": state.plan,
        "papers": state.papers,
        "messages": state.messages
    }


# Writer node: summarize everything
async def writer_node(state: State, runtime: Runtime) -> Dict:
    model = load_chat_model(runtime.context)
    system_prompt = WRITER_PROMPT.strip() + "\n\nReturn ONLY a JSON object matching the LiteratureSummary schema."

    author_stats_str = json.dumps(state.author_stats, indent=2) if state.author_stats else "N/A"

    result = await model.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""
Plan:
{state.plan.model_dump_json(indent=2)}

Papers:
{json.dumps(state.papers, indent=2)}

Author Stats:
{author_stats_str}
"""}
    ])

    print("\nRAW LLM SUMMARY OUTPUT:\n", result.content)

    try:
        summary = LiteratureSummary.model_validate_json(result.content)
        return {"summary": summary}
    except Exception as e:
        print("Error validating summary:", e)
        raise ValueError(f"Writer node failed: {e}\nOutput: {result.content}")


# NEW: Formatter node to produce human-readable report
async def formatter_node(state: State, runtime: Runtime) -> Dict:
    model = load_chat_model(runtime.context)
    system_prompt = FORMATTER_PROMPT.strip()

    result = await model.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{json.dumps(state.summary.model_dump(), indent=2)}"}
    ])

    print("\n FORMATTED REPORT:\n", result.content)

    return {
        "summary": state.summary,
        "formatted_text": result.content
    }


# Build the graph
builder = StateGraph(State, input_schema=InputState)

builder.add_node("planner", planner_node)
builder.add_node("openalex", openalex_node)
builder.add_node("author_stats", author_stats_node)
builder.add_node("writer", writer_node)
builder.add_node("formatter", formatter_node)  # NEW

builder.set_entry_point("planner")

# Conditional logic: check if author stats are needed
def route_from_openalex(state: State) -> str:
    if state.plan and state.plan.need_author_stats:
        return "author_stats"
    else:
        return "writer"

builder.add_edge("planner", "openalex")
builder.add_conditional_edges("openalex", route_from_openalex)
builder.add_edge("author_stats", "writer")
builder.add_edge("writer", "formatter")  # NEW

graph = builder.compile()

