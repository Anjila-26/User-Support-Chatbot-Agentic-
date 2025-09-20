from typing import TypedDict

from app.tools.appointment_tool import AppointmentTool
from app.tools.data_tool import DataTool
from app.tools.inference_tool import InferenceTool
from langgraph.graph import END, START, StateGraph


# Define state
class ChatState(TypedDict):
    query: str
    intent: str
    confidence: float
    response: str
    appointment_action: str
    datetime: str
    conversation_state: dict


# Initialize tools
tool = InferenceTool()
appt_tool = AppointmentTool()
rag_tool = DataTool()


# Define nodes
def intent_analysis(state: ChatState):
    result = tool.predict_and_respond(state["query"])
    state["intent"] = result["intent"]
    state["confidence"] = result["confidence"]
    state["response"] = result["response"]

    # Improve intent detection with keyword fallback
    query_lower = state["query"].lower()

    # Check for booking keywords
    booking_keywords = ["book", "schedule", "appointment", "reserve"]
    service_keywords = [
        "massage",
        "thai",
        "swedish",
        "deep tissue",
        "hot stone",
    ]

    if any(word in query_lower for word in booking_keywords) and any(
        word in query_lower for word in service_keywords
    ):
        state["intent"] = "book_service"
        state["response"] = "I'd be happy to help you book that massage!"

    # Check conversation state for pending actions
    if state.get("conversation_state", {}).get("pending") == "reschedule":
        state["intent"] = "provide_datetime"

    return state


def data_retrieval(state: ChatState):
    if state["intent"] == "pricing_inquiry":
        rag_result = rag_tool.retrieve_and_generate(state["query"])
        state["response"] = rag_result
    return state


def appointment_trigger(state: ChatState):
    user_id = state.get("conversation_state", {}).get("user_id", "user123")

    if state["intent"] in [
        "book_service",
        "reschedule_booking",
        "cancel_booking",
    ]:
        state["appointment_action"] = state["intent"]
        state["datetime"] = (
            tool.extract_datetime(state["query"]) or "Not extracted"
        )

        if state["intent"] == "book_service":
            # Extract service type from query
            query_lower = state["query"].lower()
            service = "General Massage"  # Default

            if "thai" in query_lower:
                service = "Thai Massage"
            elif "swedish" in query_lower:
                service = "Swedish Massage"
            elif "deep tissue" in query_lower:
                service = "Deep Tissue Massage"
            elif "hot stone" in query_lower:
                service = "Hot Stone Massage"
            elif "neck" in query_lower or "shoulder" in query_lower:
                service = "Neck and Shoulder Massage"
            elif "aromatherapy" in query_lower:
                service = "Aromatherapy Massage"
            elif "sports" in query_lower:
                service = "Sports Massage"
            elif "prenatal" in query_lower:
                service = "Prenatal Massage"

            result = appt_tool.add_appointment(
                user_id, service, state["datetime"]
            )
            appointments = appt_tool.get_appointments(user_id)
            latest_appt_id = (
                max([appt[0] for appt in appointments]) if appointments else 1
            )
            state["response"] = (
                f"Great! Appointment #{latest_appt_id} booked successfully for {service} on {state['datetime']}."
            )

        elif state["intent"] == "reschedule_booking":
            appointments = appt_tool.get_appointments(user_id)
            pending_appointments = [
                appt for appt in appointments if appt[4] == "pending"
            ]
            if pending_appointments:
                appointment_id = pending_appointments[-1][0]
                result = appt_tool.reschedule_appointment(
                    appointment_id, state["datetime"]
                )
                state["response"] = (
                    f"Appointment #{appointment_id} rescheduled successfully to {state['datetime']}."
                )
            else:
                state["response"] = (
                    "No pending appointments found to reschedule."
                )

        elif state["intent"] == "cancel_booking":
            appointments = appt_tool.get_appointments(user_id)
            pending_appointments = [
                appt for appt in appointments if appt[4] == "pending"
            ]
            if pending_appointments:
                appointment_id = pending_appointments[-1][0]
                result = appt_tool.cancel_appointment(appointment_id)
                state["response"] = "Appointment cancelled successfully."
            else:
                state["response"] = "No pending appointments found to cancel."

    elif state["intent"] == "booking_status":
        appointments = appt_tool.get_appointments(user_id)
        if appointments:
            count = len(appointments)
            latest = appointments[-1]
            state["response"] = (
                f"You have {count} booking(s). Your most recent: {latest[2]} on {latest[3]} (Status: {latest[4]})"
            )
        else:
            state["response"] = "You have no bookings yet."
    elif state["intent"] == "confirm":
        if state.get("conversation_state", {}).get("pending") == "reschedule":
            # Perform reschedule
            result = appt_tool.reschedule_appointment(1, state["datetime"])
            state["response"] = (
                f"Sent reschedule information to pro, you will get notified once it's confirmed. {result}"
            )
            state["conversation_state"] = {}
    elif state["intent"] == "reschedule_booking":
        state["response"] = (
            "Sure, let's reschedule. Provide the new date and time."
        )
        state["conversation_state"] = {"pending": "reschedule"}
    return state


# Build graph
graph = StateGraph(ChatState)
graph.add_node("intent_analysis", intent_analysis)
graph.add_node("data_retrieval", data_retrieval)
graph.add_node("appointment_trigger", appointment_trigger)
graph.add_edge(START, "intent_analysis")
graph.add_edge("intent_analysis", "data_retrieval")
graph.add_edge("data_retrieval", "appointment_trigger")
graph.add_edge("appointment_trigger", END)

# Compile and run
compiled_graph = graph.compile()

# Example usage
if __name__ == "__main__":
    state = {"query": "Can I reschedule my booking?", "conversation_state": {}}
    result = compiled_graph.invoke(state)
    print(result)