from fastapi import FastAPI, Request, HTTPException, Response
from app.state import AskResponse, AskQuestion
app = FastAPI()

@app.post('/ask')
async def get_response(req: AskQuestion):
    return Response.body({
        "message": "server running"
    })

