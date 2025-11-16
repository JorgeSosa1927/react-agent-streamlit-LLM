# Literature Review Assistant (LangGraph + LangChain)

This project implements a small but reliable LLM workflow using **LangGraph** and **LangChain**.

---

## What it does

Given a user query like:

> “Give me a short overview of recent work on quantum computing.”

The system:

* Extracts a structured research plan.
* Searches for recent papers (via OpenAlex API).
* Optionally analyzes author statistics.
* Summarizes the findings using an LLM.

All results are returned as **structured JSON**.

---

## Features

* ReAct pattern (reason → act → observe)
* LLM agents with clear roles (Planner, Writer)
* LangGraph with branching and conditional nodes
* Retry logic on API calls (OpenAlex)
* Pydantic models for structured input/output
* Parallel execution of tools when needed

---

## Project Structure

```text
react-agent/
│
├── src/react_agent/
│   ├── graph.py        # Main LangGraph pipeline
│   ├── prompts.py      # LLM role prompts
│   ├── tools.py        # Tool logic (OpenAlex API, author stats)
│   ├── models.py       # Pydantic schemas
│   ├── state.py        # LangGraph state definitions
│   ├── context.py      # Model context (model name, API key, etc.)
│   ├── utils.py        # Utilities (load_chat_model)
│
├── tests/
│   ├── test_graph.py   # Full end-to-end test
│
├── .env                # Optional: API keys
├── requirements.txt    # Python dependencies
├── pyproject.toml      # (Optional) build config
├── langgraph.json      # LangGraph config
├── README.md           # This file
```

---

## Requirements

* Python >= 3.10

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your `.env` file (if using OpenAI, etc.):

```env
OPENAI_API_KEY=sk-...
```

---

## ▶Run the full flow

Run the full LLM workflow with a predefined test input:

```bash
PYTHONPATH=src python -m tests.test_graph
```

You’ll see output like:

```json
{
  "topic": "Advances in Quantum Computing",
  "trends": ["..."],
  "notable_papers": [],
  "open_questions": ["..."]
}
```

---

## Mermaid Graph Diagram

```mermaid
graph TD
    A[PlannerNode: generate LiteraturePlan] --> B{need_author_stats?}
    B -- Yes --> C[AuthorStatsNode: mocked author stats]
    B --> D[OpenAlexNode: fetch real papers (retry)]
    C --> E[WriterNode: summarize findings]
    D --> E
    E --> F[Final Output: LiteratureSummary]
```

---

## License

MIT License

---

## Author

Built by **Jorge Sosa** as part of a LangGraph lab project.
