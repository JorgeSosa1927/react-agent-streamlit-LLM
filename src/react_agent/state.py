from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence, Optional
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import Annotated

from react_agent.models import LiteraturePlan, LiteratureSummary  # IMPORTAR TAMBIÉN ESTA

@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)

@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
    plan: Optional[LiteraturePlan] = None
    papers: Optional[list[dict]] = None
    summary: Optional[LiteratureSummary] = None  # AGREGALO ACÁ
    author_stats: Optional[dict] = None  # Nuevo campo para almacenar resultados
    formatted_text: Optional[str] = None   # <---- ADD THIS


