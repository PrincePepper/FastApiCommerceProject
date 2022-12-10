from uuid import UUID

from pydantic import BaseModel


# Shared properties
class RoadPointBase(BaseModel):
    name: str
    id: UUID


class RoadPointCreate(RoadPointBase):
    name: str
    id: UUID


class RoadPointUpdate(RoadPointBase):
    name: str
    id: UUID


class RoadPointInDBBase(RoadPointBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class RoadPoint(RoadPointInDBBase):
    pass


# Additional properties stored in DB
class RoadPointInDB(RoadPointInDBBase):
    pass
