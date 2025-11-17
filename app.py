import sys
from pathlib import Path

# -------------------------------------------------
# AÑADIR src/ AL PYTHONPATH PARA QUE FUNCIONE REACT_AGENT
# -------------------------------------------------
ROOT = Path(__file__).resolve().parent          # carpeta del proyecto
SRC = ROOT / "src"                              # carpeta src/

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# -------------------------------------------------
# IMPORTS NORMALES
# -------------------------------------------------
import asyncio
import streamlit as st
from langchain_core.messages import HumanMessage

from react_agent.graph import graph
from react_agent.state import InputState
from react_agent.context import Context


# -------------------------------------------------
# FUNCIÓN ASÍNCRONA QUE EJECUTA EL GRAFO
# -------------------------------------------------
async def run_graph_async(query: str):
    input_state = InputState(
        messages=[HumanMessage(content=query)]
    )
    context = Context(model="qwen3-32b")
    context.max_search_results = 5

    # LangGraph async
    result = await graph.ainvoke(input_state, context=context)
    return result


def run_graph_sync(query: str):
    """Wrapper síncrono para usar en Streamlit."""
    return asyncio.run(run_graph_async(query))


# -------------------------------------------------
# INTERFAZ STREAMLIT
# -------------------------------------------------
st.set_page_config(page_title="Literature Review Assistant", layout="wide")
st.title("📚 Literature Review Assistant")

st.markdown(
    "Este demo usa LangGraph + LangChain para hacer un pequeño flujo de "
    "literature review (planner → tools → writer → formatter)."
)

default_query = "Give me a summary of recent research on quantum computing."
user_query = st.text_area("User query:", value=default_query, height=80)

if st.button("Run Agent"):
    with st.spinner("Running LLM pipeline..."):
        result = run_graph_sync(user_query)

    st.subheader("🔍 User Query")
    st.code(user_query)

    if result.get("plan"):
        st.subheader("🧠 Extracted Research Plan (LiteraturePlan)")
        st.json(result["plan"].model_dump())

    if result.get("summary"):
        st.subheader("📊 JSON Summary (LiteratureSummary)")
        st.json(result["summary"].model_dump())

    if result.get("formatted_text"):
        st.subheader("📝 Formatted Report")
        st.markdown(result["formatted_text"])
else:
    st.info("Escribe una pregunta (o deja la default) y haz clic en **Run Agent**.")
