import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from modules.chat_engine import get_chat_response

app = FastAPI(title="Bangla/English RAG Chatbot")

class ChatRequest(BaseModel):
    query: str
    session_id: str = None
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    answer: str
    session_id: str

@app.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())[:8]
    user_id = req.user_id or "anonymous"
    answer = await get_chat_response(req.query, session_id, user_id)
    return ChatResponse(answer=answer, session_id=session_id) 