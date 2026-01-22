from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FaceRegisterRequest(BaseModel):
    """Request body for registering user face"""
    image_data: str  # Base64 encoded image


class FaceVerifyRequest(BaseModel):
    """Request body for verifying face"""
    image_data: str  # Base64 encoded image
    election_id: int  # For voting context


class FaceVerifyResponse(BaseModel):
    """Response for face verification"""
    is_match: bool
    confidence_distance: float
    message: str


class FaceEncodingResponse(BaseModel):
    """Response for face encoding"""
    id: int
    user_id: int
    confidence_score: float
    is_verified: str
    created_at: datetime

    class Config:
        from_attributes = True


class FaceStatusResponse(BaseModel):
    """Response for face verification status"""
    has_face_registered: bool
    is_verified: bool
    last_used_at: Optional[datetime]
    created_at: Optional[datetime]
