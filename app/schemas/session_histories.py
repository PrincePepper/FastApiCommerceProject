from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class SessionHistoriesBase(BaseModel):
    user_id: UUID = None
    start: str = None
    end: str = None


class SessionHistoriesCreate(SessionHistoriesBase):
    user_id: UUID
    start: str


class SessionHistoriesClose(SessionHistoriesBase):
    name: Optional[str] = None


class SessionInDBBase(SessionHistoriesBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class Session(SessionInDBBase):
    pass
