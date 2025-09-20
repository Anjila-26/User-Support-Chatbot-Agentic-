from datetime import datetime
from typing import Any, Dict

from app.chatbot_workflow import compiled_graph
from app.models.schemas import ChatResponse


class ChatbotService:
    def __init__(self):
        self.compiled_graph = compiled_graph

    def process_message(
        self, message: str, user_id: str, conversation_state: Dict[str, Any]
    ) -> ChatResponse:
        # Prepare state for the LangGraph workflow
        state = {
            "query": message,
            "conversation_state": {**conversation_state, "user_id": user_id},
        }

        # Invoke the compiled graph
        result = self.compiled_graph.invoke(state)

        # Return the response in the expected format
        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            confidence=result["confidence"],
            conversation_state=result.get("conversation_state", {}),
            timestamp=datetime.now(),
        )