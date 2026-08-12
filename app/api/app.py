from fastapi import FastAPI, Request, HTTPException, Response
from app.state import AskResponse, AskQuestion, GraphState
from app.graph import app_graph

app = FastAPI()

@app.post("/ask", response_model=AskResponse)
def askquestion(req: AskQuestion):

    initial_state: GraphState = {
        "retry_count": 0,
        "question": req.question
    }

    print(f"Asking: {req.question}")
    final = app_graph.invoke(initial_state) 

    trace_info = {
        "final_grade": final.get('grade'),
        "retries": final.get('retry_count')
    }

    return AskResponse(
        answer=final.get("answer", ""),
        citations= final.get('citations', []),
        trace=trace_info
    )

    



