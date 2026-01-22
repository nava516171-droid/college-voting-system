from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.election import ElectionStatus


class ElectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class ElectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[ElectionStatus] = None


class ElectionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: ElectionStatus
    start_time: datetime
    end_time: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
