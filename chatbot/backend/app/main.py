from app.api import chatbot
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Customer Support Chatbot API",
    description="Backend API for Customer Support Chatbot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot.router, prefix="/api/v1", tags=["chatbot"])

@app.get("/")
def read_root():
    return {"message": "Customer Support API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}