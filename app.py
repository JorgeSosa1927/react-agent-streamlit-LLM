import sys
import os

# Agrega el path para que funcione con Streamlit
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
import asyncio
from langchain_core.messages import HumanMessage

from react_agent.graph import graph
from react_agent.state import InputState
from react_agent.context import Context


async def run_graph():
    input_state = InputState(
        messages=[
            HumanMessage(content="Give me a summary of recent research on quantum computing.")
        ]
    )
    context = Context(model="qwen3-32b")
    context.max_search_results = 5
    return await graph.ainvoke(input_state, context=context)


st.set_page_config(page_title="Literature Review Assistant", layout="wide")

st.title("📚 Literature Review Assistant")

if st.button("Run Agent"):
    with st.spinner("Running LLM pipeline..."):
        result = asyncio.run(run_graph())

    st.subheader("🔍 User Query")
    st.code("Give me a summary of recent research on quantum computing.")

    if result.get("plan"):
        st.subheader("🧠 Extracted Research Plan")
        st.json(result["plan"].model_dump())

    if result.get("summary"):
        st.subheader("📊 JSON Summary")
        st.json(result["summary"].model_dump())

    if result.get("formatted_text"):
        st.subheader("📝 Formatted Report")
        st.markdown(result["formatted_text"])
else:
    st.info("Click the button to run the LLM pipeline.")

