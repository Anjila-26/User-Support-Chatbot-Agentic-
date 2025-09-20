import pickle
import re

import torch
from dateutil import parser
from transformers import DistilBertForSequenceClassification


class InferenceTool:
    def __init__(self, model_path=None):
        if model_path is None:
            import os

            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(
                current_dir, "..", "model", "chatbot_model.pkl"
            )
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        self.tokenizer = model_data["tokenizer"]
        self.label_encoder = model_data["label_encoder"]
        self.reverse_label_encoder = model_data["reverse_label_encoder"]

        num_labels = len(self.label_encoder)
        self.model = DistilBertForSequenceClassification.from_pretrained(
            "distilbert-base-uncased", num_labels=num_labels
        )
        self.model.load_state_dict(model_data["model_state_dict"])
        self.model.eval()

    def predict_intent(self, text):
        inputs = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=128,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_label = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_label].item()

        intent = self.reverse_label_encoder[predicted_label]
        return intent, confidence

    def extract_datetime(self, text):
        try:
            parsed_date = parser.parse(text, fuzzy=True)
            standardized = parsed_date.strftime("%Y-%m-%d %H:%M")
            return standardized
        except ValueError:
            return None

    def predict_and_respond(self, text):
        intent, confidence = self.predict_intent(text)

        responses = {
            "greeting": "Hello! How can I help with your booking?",
            "reschedule_booking": "Sure, let's reschedule. Provide the new date and time.",
            "cancel_booking": "Got it. Confirm if you want to cancel.",
            "pricing_inquiry": "Let me check the prices.",
            "book_service": "I'd be happy to book. What type and when?",
            "booking_status": "Please provide your booking reference.",
            "thanks": "You're welcome!",
            "confirm": "Confirmed!",
            "deny": "No problem.",
            "provide_datetime": "Noted the time.",
        }

        response = responses.get(
            intent, "I'm sorry, I didn't understand that."
        )
        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
        }