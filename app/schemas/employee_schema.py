"""
This file defines Pydantic Schemas used as an Anti-Corruption Layer.
These schemas strictly validate incoming request payloads and format outgoing 
responses. They ensure that no malformed data ever reaches the Service layer 
or the database.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class EmployeeCreateSchema(BaseModel):
    """
    Schema for validating employee creation payloads (POST).
    Requires all fields to establish a complete record.
    """
    name: str = Field(..., min_length=1, description="Employee's full name")
    email: EmailStr = Field(..., description="Employee's email address")
    department: str = Field(..., min_length=1, description="Department name")
    date_joined: Optional[datetime] = Field(None, description="Date the employee joined")

class EmployeeUpdateSchema(BaseModel):
    """
    Schema for validating employee update payloads (PATCH).
    All fields are optional to support partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, description="Employee's full name")
    email: Optional[EmailStr] = Field(None, description="Employee's email address")
    department: Optional[str] = Field(None, min_length=1, description="Department name")
    date_joined: Optional[datetime] = Field(None, description="Date the employee joined")

class EmployeeResponseSchema(BaseModel):
    """
    Schema for serializing SQLAlchemy employee data back to JSON.
    """
    id: int
    name: str
    email: EmailStr
    department: str
    date_joined: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
