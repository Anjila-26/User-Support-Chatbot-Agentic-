from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Customer Support Chatbot"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: Optional[str] = None

    # AI/ML Settings
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"


settings = Settings()