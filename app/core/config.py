from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    APP_ENV: str = "development"
    GROQ_MODEL: str

    class Config:
        env_file = ".env"

settings = Settings()