from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CandidateCreate(BaseModel):
    election_id: int
    name: str
    symbol_number: int
    description: Optional[str] = None
    email: Optional[str] = None


class CandidateResponse(BaseModel):
    id: int
    election_id: int
    name: str
    symbol_number: int
    description: Optional[str]
    email: Optional[str]
    campaign_message: Optional[str]
    about: Optional[str]
    poster: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
