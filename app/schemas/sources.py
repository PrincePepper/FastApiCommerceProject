from typing import Optional

from pydantic import BaseModel, Json


# Shared properties
class SourceBase(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    properties: Optional[Json] = None


class SourceCreate(SourceBase):
    id: str
    name: str
    address: str
    properties: Json


class SourceUpdateName(SourceBase):
    name: Optional[str] = None


class SourceUpdateAddress(SourceBase):
    address: Optional[str] = None


class SourceUpdateProperties(BaseModel):
    id: Optional[str] = None
    properties: Optional[Json] = None


class SourceInDBBase(SourceBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class Source(SourceInDBBase):
    pass
