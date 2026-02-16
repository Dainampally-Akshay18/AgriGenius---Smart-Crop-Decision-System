"""
User request/response schemas.
"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""
    
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    """User login request."""
    
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Authentication response with token."""
    
    message: str
    token: str
    user: dict


class ErrorResponse(BaseModel):
    """Error response."""
    
    error: bool = True
    code: int
    message: str
