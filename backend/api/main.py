"""
HispeedCity AI Assistant - ChatBot API Server

Exposes HTTP API endpoints for web chatbot widget.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional
from twilio.twiml.messaging_response import MessagingResponse

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.chatbot.chatbot import ChatBot

app = FastAPI(title="HispeedCity AI ChatBot API")

# Enable CORS for local and web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatBot instance
chatbot = ChatBot()


class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or prompt")
    session_id: Optional[str] = Field(default="default", description="User session identifier")


class ChatResponse(BaseModel):
    answer: str
    intent: str
    confidence: float
    requires_plate: Optional[bool] = False
    vehicle_plate: Optional[str] = None
    portal_status: Optional[str] = None


# Session Memory Store (In-Memory)
session_store = {}


@app.get("/")
async def root():
    return {"message": "HispeedCity AI ChatBot API is active."}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    session_id = request.session_id or "default"
    
    # Retrieve existing session context
    context = session_store.get(session_id, {})

    # Pass context to chatbot
    result = chatbot.ask(request.message.strip(), context=context)

    # Update context with new information
    if result.get("vehicle_plate"):
        context["vehicle_plate"] = result.get("vehicle_plate")
    if result.get("intent"):
        context["intent"] = result.get("intent")
    
    session_store[session_id] = context

    return ChatResponse(
        answer=result.get("answer", ""),
        intent=result.get("intent", "general"),
        confidence=result.get("confidence", 1.0),
        requires_plate=result.get("requires_plate", False),
        vehicle_plate=result.get("vehicle_plate"),
        portal_status=result.get("portal_status"),
    )


@app.post("/api/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Twilio WhatsApp Webhook.
    Receives incoming WhatsApp messages, processes them via ChatBot,
    and returns a TwiML response.
    """
    form_data = await request.form()
    
    incoming_msg = form_data.get("Body", "").strip()
    sender_id = form_data.get("From", "whatsapp_default")
    
    # Twilio sends numbers like "whatsapp:+123456789"
    # We use this as the session_id for conversational memory
    session_id = sender_id
    
    context = session_store.get(session_id, {})
    
    # Process message
    result = chatbot.ask(incoming_msg, context=context)
    
    # Update memory
    if result.get("vehicle_plate"):
        context["vehicle_plate"] = result.get("vehicle_plate")
    if result.get("intent"):
        context["intent"] = result.get("intent")
    
    session_store[session_id] = context
    
    answer = result.get("answer", "Sorry, I could not understand your request.")
    
    # Build TwiML response
    twiml = MessagingResponse()
    twiml.message(answer)
    
    return PlainTextResponse(str(twiml), media_type="application/xml")


