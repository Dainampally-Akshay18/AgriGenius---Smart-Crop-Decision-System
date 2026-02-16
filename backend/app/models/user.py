"""
User data model for Firestore.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model matching Firestore schema."""
    
    id: Optional[str] = None
    name: str
    email: EmailStr
    password_hash: str
    created_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserCreate(BaseModel):
    """User creation model (without hash)."""
    
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model (without password)."""
    
    id: str
    name: str
    email: EmailStr
    created_at: datetime
