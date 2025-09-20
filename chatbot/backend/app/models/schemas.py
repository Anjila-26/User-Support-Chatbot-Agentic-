from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_state: Optional[Dict[str, Any]] = {}


class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    conversation_state: Dict[str, Any]
    timestamp: datetime


class AppointmentCreate(BaseModel):
    service_type: str
    date: str
    time: str
    duration: Optional[int] = 60
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: str
    service_type: str
    date: str
    time: str
    status: str
    created_at: datetime


class ServiceInfo(BaseModel):
    name: str
    price: float
    duration: int
    description: str
