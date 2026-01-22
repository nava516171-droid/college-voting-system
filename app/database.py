from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Use SQLite as a fallback if PostgreSQL is not available
db_url = settings.DATABASE_URL
if not db_url or "postgresql" in db_url:
    # Use SQLite for testing/demo
    db_url = "sqlite:///./voting_system.db"

engine = create_engine(
    db_url, 
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
