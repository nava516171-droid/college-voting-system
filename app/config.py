import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/college_voting_db"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True
    
    # Frontend URL - Change this for production/phone access
    # For mobile access, set FRONTEND_URL to http://<your-machine-ip>:3000
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Email Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"  # Use Gmail App Password, not regular password
    SENDER_NAME: str = "College Voting System"
    SENDER_EMAIL: str = "your-email@gmail.com"

    class Config:
        env_file = ".env"


settings = Settings()
