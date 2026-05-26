from pydantic import BaseModel, Field
from typing import Literal


class WikiSection(BaseModel):
    heading: str
    content: str


class WikiPage(BaseModel):
    id: str
    title: str
    type: Literal["player", "concept"]
    position: str = ""
    nationality: str = ""
    summary: str
    sections: list[WikiSection]
    related: list[str] = []
    tags: list[str] = []
    quality_score: int = 0


class EvaluationResult(BaseModel):
    score: int = Field(ge=1, le=5)
    improvements: list[str]


class GraphNode(BaseModel):
    id: str
    label: str
    type: Literal["player", "concept"]
    size: int


class GraphLink(BaseModel):
    source: str
    target: str
    strength: float = 1.0


class WikiGraph(BaseModel):
    nodes: list[GraphNode]
    links: list[GraphLink]


class WikiData(BaseModel):
    players: list[WikiPage]
    concepts: list[WikiPage]
    graph: WikiGraph
    built_at: str
