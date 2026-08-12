from typing import List, Dict, Any, TypedDict, Literal
from pydantic import BaseModel, Field

class GraphState(TypedDict):
    question: str
    search_query: str
    documents: List[Dict[str, Any]]
    grade: Literal["SUFFICIENT" , "INSUFFICIENT" , "NOT_FOUND"] 
    grade_reason: str
    rewrite_query: str
    retry_count: int
    answer: str
    citations: List[str]
    trace: Dict[str, Any]

class GradeDocumentsOutput(BaseModel):
    grade: Literal["SUFFICIENT" , "INSUFFICIENT" , "NOT_FOUND"] = Field(description='Grade the chunks based on relevance only ')
    reason: str = Field(description="Brief explanation for the grade.")
    rewrite_query: str = Field(default="",
        description="If grade is 'insufficient', a rephrased search query optimized for vector search. Otherwise empty.")

class AskQuestion(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    ciatation: List[str]
    trace: Dict[str, Any]

