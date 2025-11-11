"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# School-related schemas

class Department(BaseModel):
    name: str = Field(..., description="Department name")
    head: Optional[str] = Field(None, description="Head of department")
    description: Optional[str] = Field(None, description="Brief about the department")

class Faculty(BaseModel):
    name: str = Field(..., description="Full name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Contact number")
    department: Optional[str] = Field(None, description="Department name")
    designation: Optional[str] = Field(None, description="Role / Title")
    bio: Optional[str] = Field(None, description="Short bio")
    photo_url: Optional[str] = Field(None, description="Profile image URL")

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event details")
    date: datetime = Field(..., description="Event date and time")
    location: Optional[str] = Field(None, description="Where it happens")
    category: Optional[str] = Field(None, description="Type (sports, cultural, academic)")

class Notice(BaseModel):
    title: str = Field(..., description="Notice headline")
    content: str = Field(..., description="Notice body")
    priority: Optional[str] = Field("normal", description="low | normal | high")
    published_at: datetime = Field(default_factory=datetime.utcnow)

class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., description="Message body")

# Example schemas kept for reference (unused by the app but valid)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
