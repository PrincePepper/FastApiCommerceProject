from uuid import UUID

from pydantic import BaseModel


# Shared properties
class RouteBase(BaseModel):
    name: str
    id: UUID
    from_id: UUID
    to_id: UUID


class RouteCreate(RouteBase):
    name: str
    id: UUID
    from_id: UUID
    to_id: UUID


class RouteUpdate(RouteBase):
    name: str
    id: UUID
    from_id: UUID
    to_id: UUID


class RouteInDBBase(RouteBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Route(RouteInDBBase):
    pass


# Additional properties stored in DB
class RouteInDB(RouteInDBBase):
    pass
