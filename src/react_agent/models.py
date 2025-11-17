# Define la estructura de los datos con Pydantic
from typing import List, Optional 
from pydantic import BaseModel # definir, validar y estructurar datos


# Salida del nodo Planner
class LiteraturePlan(BaseModel):
    keywords: List[str]
    min_year: int
    need_author_stats: bool
    
# Resultado de buscar un paper en arXiv
class PaperInfo(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    year: Optional[int] = None

# Estadísticas de autor si se requieren
class AuthorStats(BaseModel):
    author: str
    h_index: Optional[int] = None


# Resultado final del Writer Node
class LiteratureSummary(BaseModel):
    topic: str
    trends: List[str]
    notable_papers: List[str]
    open_questions: List[str]