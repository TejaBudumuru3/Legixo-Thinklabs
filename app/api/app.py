from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.state import AskResponse, AskQuestion, GraphState
from app.graph import app_graph

app = FastAPI(title="Legixo Thinklabs Legal Q&A API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask", response_model=AskResponse)
def askquestion(req: AskQuestion):
    try:
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
    except Exception as e:
        error_msg = str(e).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            raise HTTPException(status_code=429, detail="Too many requests from LLM. Please try again later.")
                    
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Mount static web chat UI if static directory exists
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


    



