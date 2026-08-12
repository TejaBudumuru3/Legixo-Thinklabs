from config import ai_client
from google.genai import types
from app.pinecone_client import query_index
from app.state import GraphState, GradeDocumentsOutput
from app.prompts import GRADER_PROMPT, ANSWER_PROMPT

def retrival(state: GraphState) -> dict:
    query_to_embed = state.get("search_query") or state.get("question")
    print("converting query into embeddings using gemini")
    result = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=query_to_embed,
        config=types.EmbedContentConfig(output_dimensionality=768, task_type='RETRIEVAL_QUERY')
    )
    print("="*30)
    print(result)
    print("="*30)
    if result.embeddings:
        embeddings = result.embeddings[0].values
        if embeddings:
            documents = query_index(embeddings)
            if documents:
                return { "documents": documents }

    return { "documents": [] }

def grade_documents(state: GraphState):
    documents = state.get('documents')
    question  = state.get('question')
    retries = state.get('retry_count', 0)

    if not documents: 
        return {
            "grade": "NOT_FOUND",
            "grade_reason": "No documents returned from Pinecone.",
            "answer": "The provided documents do not contain sufficient information to answer this question.",
            "citations": []
        }
    
    if retries >=3:
        return {
            "grade": "NOT_FOUND",
            "grade_reason": "No documents returned from Pinecone.",
            "answer": "The provided documents do not contain sufficient information to answer this question.",
            "citations": []
        }
    

    context = "\n\n".join([doc['metadata']['text']  for doc in documents])

    prompt = GRADER_PROMPT.format(question=question, context=context)

    res = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GradeDocumentsOutput,
            temperature=0.0
        )
    )

    print("="*30)
    print(res)
    print("="*30)
    parsed_grade: GradeDocumentsOutput = res.parsed  # type: ignore

    update_dict: dict = {
        "grade": parsed_grade.grade,
        "grade_reason": parsed_grade.reason
    }

    if parsed_grade.grade == "INSUFFICIENT" and parsed_grade.rewrite_query:
        update_dict['search_query'] = parsed_grade.rewrite_query
        update_dict['retry_count'] = retries + 1
    
    if parsed_grade.grade == 'NOT_FOUND':
        update_dict["answer"] = "The provided documents do not contain sufficient information to answer this question."
        update_dict["citations"] = []

    return update_dict

def generate_answer(state: GraphState):
    question = state["question"]
    documents = state["documents"]
    context = "\n\n".join([doc['metadata']['text'] for doc in documents])

    citation = list(set([doc['metadata']['source'] for doc in documents]))

    prompt = ANSWER_PROMPT.format(question=question, context= context)

    res = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    print("="*30)
    print(res)
    print("="*30)

    return {
        "answer": res.text,
        "citations": citation
    }