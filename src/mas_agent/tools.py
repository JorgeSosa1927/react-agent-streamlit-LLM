from typing import Dict, Any
import asyncio

from langchain_core.messages import HumanMessage

from react_agent.graph import graph
from react_agent.state import InputState
from react_agent.context import Context


def run_research_assistant(query: str, memory: list | None = None) -> Dict[str, Any]:
    """
    Wrapper sincronizado alrededor del grafo de Lab 1.

    Internamente hace lo mismo que tests/test_graph.py:
    - Crea un InputState con un HumanMessage
    - Crea un Context con el modelo qwen3-32b
    - Llama a graph.ainvoke(...)
    - Normaliza la salida a un dict con claves:
        plan, summary_json, formatted_report, papers
    """
    if memory is None:
        memory = []

    input_state = InputState(
        messages=[
            HumanMessage(content=query)
        ]
    )

    context = Context(model="qwen3-32b")
    context.max_search_results = 15

    async def _run():
        return await graph.ainvoke(input_state, context=context)

    # Ejecutamos el grafo asíncrono de Lab1 de forma síncrona
    result = asyncio.run(_run())

    plan_obj = result.get("plan")
    summary_obj = result.get("summary")
    formatted = result.get("formatted_text")

    plan = plan_obj.model_dump() if hasattr(plan_obj, "model_dump") else plan_obj
    summary_json = (
        summary_obj.model_dump() if hasattr(summary_obj, "model_dump") else summary_obj
    )

    # "papers" puede llamarse distinto en tu grafo; ajusta si hace falta
    papers = result.get("papers") or result.get("openalex_results") or []

    return {
        "plan": plan,
        "summary_json": summary_json,
        "formatted_report": formatted or "",
        "papers": papers,
    }
