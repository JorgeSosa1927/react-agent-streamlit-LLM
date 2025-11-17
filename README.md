# ANLP2025 – Literature Review Agent (LangGraph + LangChain)

This project is part of **Lab #1** for the **ANLP2025** course.  
It implements a modular, multi-step LLM agent using **LangGraph** and **LangChain** to automate literature reviews.

---

## 📌 What it does

Given a user query like:

> “Give me a short overview of recent work on quantum computing.”

the system:

1. Extracts a **structured research plan** (keywords, year filter, need for author stats).
2. Searches for **recent papers** using the OpenAlex API.
3. Optionally analyzes **author statistics** (mocked tool).
4. Summarizes the findings using a **Large Language Model (LLM)**.
5. Produces both:
   - A **JSON summary** (`LiteratureSummary`).
   - A **formatted natural-language report** (via a Formatter LLM).

All intermediate steps use **Pydantic models** as data contracts.

---

## ✨ Features

- ✅ ReAct-style pattern (reason → act → observe → reason again)
- ✅ LLM agents with clear roles:
  - **Planner** (builds `LiteraturePlan`)
  - **Writer** (builds `LiterureSummary`)
  - **Formatter** (converts JSON summary to a human-readable paragraph)
- ✅ LangGraph `StateGraph` with:
  - Parallel tool branches (`openalex` + `author_stats`)
  - State merging before the writer node
- ✅ Retry logic (`tenacity`) for external API calls to OpenAlex
- ✅ Pydantic models for strict input/output validation
- ✅ Streamlit UI for interactive exploration

---

## 🗂 Project Structure

```text
anlp2025-lab1-jorge-sosa/
│
├── src/react_agent/
│   ├── graph.py        # LangGraph pipeline logic
│   ├── prompts.py      # LLM prompts for planner/writer/formatter
│   ├── tools.py        # External tool integrations (OpenAlex, stats)
│   ├── models.py       # Pydantic schemas for validation
│   ├── state.py        # Graph state definitions
│   ├── context.py      # Model context: keys, model type, etc.
│   ├── utils.py        # Shared helpers (e.g., load_chat_model)
│
├── tests/
│   └── test_graph.py   # Full end-to-end test
│
├── .env                # Environment variables (e.g., OpenAI API key)
├── requirements.txt    # Project dependencies
├── pyproject.toml      # Optional build config
├── langgraph.json      # LangGraph configuration (if used)
├── README.md           # This file
├── app.py              # Streamlit interface
```

---

## 📦 Requirements

- Python **≥ 3.10**

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate          # On Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Set up your `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=sk-...
```

---

## ▶ Running the Agent

### ➤ Option 1: Run via terminal (end-to-end test)

```bash
PYTHONPATH=src python -m tests.test_graph
```

This will:

- Run the LangGraph workflow on a sample query
- Print:
  - The extracted `LiteraturePlan`
  - The JSON `LiteratureSummary`
  - The final formatted report

### ➤ Option 2: Run with Streamlit UI

```bash
python -m streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`) and:

1. Type a query (e.g. *“Give me a short overview of recent work on quantum computing.”*).
2. Click **Run Agent**.
3. Inspect:
   - The extracted research plan (Pydantic `LiteraturePlan`).
   - The JSON summary (`LiteratureSummary`).
   - The final formatted paragraph.

Example of JSON summary:

```json
{
  "topic": "Advances in Quantum Computing",
  "trends": ["..."],
  "notable_papers": ["..."],
  "open_questions": ["..."]
}
```

---

## 🧠 LangGraph Execution Flow

```mermaid
graph TD
  A[Planner Node<br/>(LLM → LiteraturePlan)] --> B[OpenAlex Node<br/>(fetch_papers_with_retry)]
  A --> C[AuthorStats Node<br/>(fetch_author_stats or None)]

  B --> D[Writer Node<br/>(LLM → LiteratureSummary)]
  C --> D

  D --> E[Formatter Node<br/>(LLM → formatted text)]
```

- **Planner**: reasons about the query and decides:
  - Which keywords to use
  - From which year to search
  - Whether author stats are needed (`need_author_stats`)
- **OpenAlex & AuthorStats**:
  - Run in **parallel**, since they do not depend on each other.
  - Their outputs are merged into the shared state before calling the writer.
- **Writer**:
  - Reads `plan`, `papers` and `author_stats`
  - Produces a structured `LiteratureSummary` (Pydantic)
- **Formatter**:
  - Converts the JSON summary into a human-readable paragraph.

---

## 🧾 License

MIT License.

---

## 👤 Author

Created by **Jorge Sosa** for the **ANLP2025** course, Lab 1.



