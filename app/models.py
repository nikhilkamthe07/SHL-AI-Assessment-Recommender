from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    query: str


class Recommendation(BaseModel):
    name: str
    category: str
    url: str


class ChatResponse(BaseModel):
    query: str
    answer: str
    recommendations: List[Recommendation]
    count: int