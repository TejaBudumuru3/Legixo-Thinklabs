from typing import List, Dict, Any, TypedDict, Literal
from pydantic import BaseModel, Field

class GraphState(TypedDict, total=False):
    question: str
    search_query: str
    documents: List[Dict[str, Any]]
    grade: Literal["SUFFICIENT" , "INSUFFICIENT" , "NOT_FOUND"] 
    grade_reason: str
    retry_count: int
    answer: str
    citations: List[str]
    trace: Dict[str, Any]

class GradeDocumentsOutput(BaseModel):
    model_config = {"extra": "forbid"}
    grade: Literal["SUFFICIENT" , "INSUFFICIENT" , "NOT_FOUND"] = Field(description='Grade the chunks based on relevance only ')
    reason: str = Field(description="Brief explanation for the grade.")
    rewrite_query: str = Field(description="If grade is 'insufficient', a rephrased search query optimized for vector search. Otherwise empty.")

class GenerateAnswerOutput(BaseModel):
    model_config = {"extra": "forbid"}
    answer: str = Field(description="The synthesized answer to the user's question.")
    cited_files: List[str] = Field(description="List of source filenames used to construct the answer.")

class AskQuestion(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    citations: List[str]
    trace: Dict[str, Any]

