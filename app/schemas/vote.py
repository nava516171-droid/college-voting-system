from pydantic import BaseModel
from datetime import datetime


class VoteCreate(BaseModel):
    election_id: int
    candidate_id: int


class VoteResponse(BaseModel):
    id: int
    user_id: int
    election_id: int
    candidate_id: int
    created_at: datetime

    class Config:
        from_attributes = True
