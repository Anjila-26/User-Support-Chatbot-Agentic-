import json
# Configuration
import os
import uuid
from datetime import datetime

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Page configuration
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="💆‍♀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {}

if "processing_message" not in st.session_state:
    st.session_state.processing_message = False

if "show_all_massages" not in st.session_state:
    st.session_state.show_all_massages = False


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_services():
    try:
        response = requests.get(f"{API_BASE_URL}/services")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        return []


@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_all_massage_types():
    """Get all massage types from the expanded dataset"""
    try:
        import os

        import pandas as pd

        # Try to read the expanded dataset
        dataset_path = "./backend/app/dataset/simple_dataset.csv"
        if not os.path.exists(dataset_path):
            dataset_path = "../backend/app/dataset/simple_dataset.csv"

        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            return df["Massage_Type"].tolist()
        else:
            return []
    except Exception as e:
        return []


def send_message(message: str):
    try:
        payload = {
            "message": message,
            "user_id": st.session_state.user_id,
            "conversation_state": st.session_state.conversation_state,
        }

        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Failed to send message: {e}")
        return None

# Sidebar
with st.sidebar:
    st.title("💆‍♀️ Customer Support AI Chatbot")
    st.markdown("### Massage Booking Assistant")

    # Backend status check (cached to avoid excessive requests)
    if "backend_status" not in st.session_state:
        try:
            health_response = requests.get(
                "http://localhost:8000/health", timeout=2
            )
            st.session_state.backend_status = (
                health_response.status_code == 200
            )
        except:
            st.session_state.backend_status = False

    if st.session_state.backend_status:
        st.success("🟢 Backend Connected")
    else:
        st.error("🔴 Backend Offline")
        if st.button("🔄 Check Connection"):
            del st.session_state.backend_status  # Force recheck
            st.rerun()

    st.markdown("---")
    st.markdown(f"**User ID:** `{st.session_state.user_id[:8]}...`")

    # Reset chat
    if st.button("🔄 New Chat"):
        st.session_state.messages = []
        st.session_state.conversation_state = {}

    
    # Show available services
    st.markdown("---")
    st.markdown("**Available Services:**")

    # Show basic service categories without prices
    services = get_services()
    if services:
        for service in services:
            st.markdown(f"• {service['name']}")
    else:
        # Fallback basic services
        basic_services = [
            "Swedish Massage",
            "Deep Tissue Massage",
            "Hot Stone Massage",
            "Neck and Shoulder Massage",
            "Aromatherapy Massage",
            "Thai Massage",
            "Sports Massage",
            "Prenatal Massage",
        ]
        for service in basic_services:
            st.markdown(f"• {service}")

    # See More button for all massage types
    if not st.session_state.show_all_massages:
        if st.button("👀 See All Massage Types"):
            st.session_state.show_all_massages = True
    else:
        # Show all massage types from expanded dataset
        all_massages = get_all_massage_types()
        if all_massages:
            st.markdown("**All Massage Types:**")
            # Display in a more compact format
            for i in range(0, len(all_massages), 2):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"• {all_massages[i]}")
                if i + 1 < len(all_massages):
                    with col2:
                        st.markdown(f"• {all_massages[i+1]}")

        if st.button("🙈 Show Less"):
            st.session_state.show_all_massages = False

# Main chat interface
st.title("💬 Chat with Customer Support AI Assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        # Show metadata for assistant messages
        if message["role"] == "assistant" and "metadata" in message:
            with st.expander("AI Analysis", expanded=False):
                metadata = message["metadata"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Intent:** {metadata.get('intent', 'N/A')}")
                with col2:
                    confidence = metadata.get("confidence", 0)
                    st.write(f"**Confidence:** {confidence:.2%}")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    if not st.session_state.processing_message:
        st.session_state.processing_message = True

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        # Send message to backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = send_message(prompt)

                if result:
                    response = result["response"]
                    intent = result["intent"]
                    confidence = result["confidence"]

                    # Update conversation state
                    st.session_state.conversation_state = result.get(
                        "conversation_state", {}
                    )

                    st.write(response)

                    # Add to message history
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "metadata": {
                                "intent": intent,
                                "confidence": confidence,
                            },
                        }
                    )
                else:
                    st.error(
                        "Failed to get response from chatbot. Please try again."
                    )

        st.session_state.processing_message = False


# Show appointments section
st.markdown("---")
if st.button("📋 View All My Appointments"):
    try:
        response = requests.get(
            f"{API_BASE_URL}/appointments/{st.session_state.user_id}"
        )
        if response.status_code == 200:
            appointments = response.json()
            if appointments:
                st.markdown("### Your Appointments")
                for appt in appointments:
                    status_emoji = (
                        "✅" if appt["status"] == "pending" else "❌"
                    )
                    st.markdown(
                        f"{status_emoji} **#{appt['id']}** - {appt['service_type']} on {appt['date']} ({appt['status']})"
                    )
            else:
                st.info("You have no appointments yet.")
        else:
            st.error("Failed to fetch appointments")
    except Exception as e:
        st.error(f"Error fetching appointments: {e}")

