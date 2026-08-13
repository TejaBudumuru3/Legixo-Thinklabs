from config import ai_client, groq_client
from google.genai import types
from app.pinecone_client import query_index
from app.state import GraphState, GradeDocumentsOutput
from app.prompts import GRADER_PROMPT, ANSWER_PROMPT

groq_model = "llama-3.3-70b-versatile"

def retrieval(state: GraphState) -> dict:
    query_to_embed = state.get("search_query") or state.get("question")
    print("converting query into embeddings using gemini")
    result = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=query_to_embed,
        config=types.EmbedContentConfig(output_dimensionality=768, task_type='RETRIEVAL_QUERY')
    )

    if result.embeddings:
        embeddings = result.embeddings[0].values
        if embeddings:
            existing_docs = state.get('documents',[])

            new_docs = query_index(embeddings)
            all_docs = existing_docs + new_docs
            unique_docs = {}
            for doc in all_docs:
                unique_docs[doc['id']] = doc
            
            unique_docs_list = list(unique_docs.values())
            unique_docs_list.sort(key=lambda x: x['score'], reverse=True)
            documents = unique_docs_list[:5]
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


    res = groq_client.chat.completions.create(
        model = groq_model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.0,
        response_format={
            "type": "json_object",
        }
    )

    raw_json_string = res.choices[0].message.content
    parsed_grade = GradeDocumentsOutput.model_validate_json(raw_json_string) # type: ignore
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
    question = state.get("question", "")
    documents = state.get("documents", [])
    context = "\n\n".join([doc['metadata']['text'] for doc in documents])

    citation = list(set([doc['metadata']['source'] for doc in documents]))

    prompt = ANSWER_PROMPT.format(question=question, context= context)

    res = groq_client.chat.completions.create(
        model= groq_model,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    answer = res.choices[0].message.content

    return {
        "answer": answer,
        "citations": citation
    }