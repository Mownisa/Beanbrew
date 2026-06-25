from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import datetime


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    code: int
    status: str
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    request_id: str
    timestamp: str


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer_id: int
    name: str
    email: str


class CustomerOut(BaseModel):
    customer_id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
