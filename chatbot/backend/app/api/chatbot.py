from typing import List

from app.models.schemas import (AppointmentResponse, ChatRequest, ChatResponse,
                                ServiceInfo)
from app.services.chatbot_service import ChatbotService
from app.tools.appointment_tool import AppointmentTool
from fastapi import APIRouter, HTTPException

router = APIRouter()
chatbot_service = ChatbotService()
appointment_tool = AppointmentTool()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = chatbot_service.process_message(
            message=request.message,
            user_id=request.user_id,
            conversation_state=request.conversation_state,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/services", response_model=List[ServiceInfo])
async def get_services():
    services = [
        ServiceInfo(
            name="Swedish Massage",
            price=85,
            duration=60,
            description="Relaxing full-body massage",
        ),
        ServiceInfo(
            name="Deep Tissue Massage",
            price=110,
            duration=60,
            description="Intense massage for muscle relief",
        ),
        ServiceInfo(
            name="Hot Stone Massage",
            price=125,
            duration=75,
            description="Massage with heated stones",
        ),
        ServiceInfo(
            name="Neck and Shoulder Massage",
            price=65,
            duration=30,
            description="Targeted upper body massage",
        ),
        ServiceInfo(
            name="Aromatherapy Massage",
            price=95,
            duration=60,
            description="Massage with essential oils",
        ),
        ServiceInfo(
            name="Thai Massage",
            price=100,
            duration=60,
            description="Traditional Thai stretching massage",
        ),
        ServiceInfo(
            name="Sports Massage",
            price=120,
            duration=60,
            description="Massage for athletes and active people",
        ),
        ServiceInfo(
            name="Prenatal Massage",
            price=90,
            duration=60,
            description="Safe massage for expecting mothers",
        ),
    ]
    return services


@router.get(
    "/appointments/{user_id}", response_model=List[AppointmentResponse]
)
async def get_user_appointments(user_id: str):
    try:
        appointments = appointment_tool.get_appointments(user_id)
        result = []
        for appt in appointments:
            # Database structure: (id, user_id, service, date_time, status)
            appointment_id = appt[0]
            appointment_user_id = appt[1]
            service_type = appt[2]
            date_time = appt[3]
            status = appt[4]

            # Handle "Not extracted" case
            if date_time == "Not extracted" or not date_time:
                date_part = "TBD"
                time_part = "TBD"
                created_at = datetime.now()
            else:
                # Split date_time if it contains both date and time
                if " " in date_time and ":" in date_time:
                    date_part, time_part = date_time.split(" ", 1)
                else:
                    date_part = date_time
                    time_part = ""

                # Handle created_at datetime
                from datetime import datetime

                try:
                    created_at = datetime.fromisoformat(
                        date_time.replace(" ", "T")
                    )
                except:
                    created_at = datetime.now()

            result.append(
                AppointmentResponse(
                    id=appointment_id,
                    user_id=appointment_user_id,
                    service_type=service_type,
                    date=date_part,
                    time=time_part,
                    status=status,
                    created_at=created_at,
                )
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching appointments: {str(e)}"
        )