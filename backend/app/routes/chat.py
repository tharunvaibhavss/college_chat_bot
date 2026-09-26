from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ChatRequest, ChatResponse
from ..services.chatbot import process_chat_message

router = APIRouter(prefix="/api", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """Primary conversational endpoint for student queries."""
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        response_data = process_chat_message(db, request.message)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal chatbot error: {str(e)}")
