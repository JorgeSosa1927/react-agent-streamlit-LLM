from typing import TypedDict, List, Literal, Optional, Dict, Any


class MASState(TypedDict, total=False):
    """
    Shared state for the Multi-Agent Study & Productivity Assistant.
    """

    user_query: str
    query_type: Optional[Literal["research", "theory", "coding", "planning"]]

    research_result: Optional[Dict[str, Any]]
    draft_answer: Optional[str]
    final_answer: Optional[str]

    agents_visited: List[str]
    tools_used: List[str]

    # cada item: {"query": str, "answer": str, "type": str}
    memory: List[Dict[str, Any]]
