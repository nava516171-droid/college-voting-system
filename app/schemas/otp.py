from pydantic import BaseModel
from datetime import datetime


class OTPRequest(BaseModel):
    email: str


class OTPVerify(BaseModel):
    otp_code: str


class OTPResponse(BaseModel):
    id: int
    user_id: int
    is_verified: bool
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
