"""Admin schemas for validation"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class AdminCreate(BaseModel):
    """Schema for creating admin"""
    email: EmailStr
    full_name: str
    password: str


class AdminLogin(BaseModel):
    """Schema for admin login"""
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    """Schema for admin response"""
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminToken(BaseModel):
    """Schema for admin token response"""
    access_token: str
    token_type: str
    admin: AdminResponse
