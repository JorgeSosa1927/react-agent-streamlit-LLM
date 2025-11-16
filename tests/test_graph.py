import asyncio
from langchain_core.messages import HumanMessage

from react_agent.graph import graph
from react_agent.state import InputState
from react_agent.context import Context


async def main():
    input_state = InputState(
        messages=[
            HumanMessage(content="Give me a summary of recent research on quantum computing.")
        ]
    )

    context = Context(model="qwen3-32b")
    context.max_search_results = 15

    result = await graph.ainvoke(input_state, context=context)

    print("\n Keys in the result:", result.keys())

    # Planner output
    print("\n Planner output:")
    plan = result.get("plan")
    if plan:
        print(plan.model_dump_json(indent=2))
    else:
        print("  No planner output found.")

    # JSON Summary from Writer
    print("\n  JSON Summary (Writer):")
    summary = result.get("summary")
    if summary:
        print(summary.model_dump_json(indent=2))
    else:
        print("  No summary found.")

    # Formatted natural language output
    print("\n  Formatted Report (Formatter):")
    formatted = result.get("formatted_text")
    if formatted:
        print(formatted)
    else:
        print(" No formatted report found.")


if __name__ == "__main__":
    asyncio.run(main())
