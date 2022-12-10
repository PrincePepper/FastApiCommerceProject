from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str]
    is_admin: bool = False
    is_active: bool = True
    created_at: int = None
    name: Optional[str]
    country_code: int = 7


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    user_id: str
    email: EmailStr = None
    phone_number: str = None
    name: Optional[str] = None
    password: str = None


class UserAccess(BaseModel):
    email: EmailStr = "admin@asuinc.ru"
    password: str = "admin"


class UserIndicatorStatus(BaseModel):
    user_id: UUID
    is_active: bool


class UserUpdate(UserBase):
    email: EmailStr = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
