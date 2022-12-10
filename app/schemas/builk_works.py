from uuid import UUID

from pydantic import BaseModel


# Shared properties
class BuilkWorkBase(BaseModel):
    data_time: int
    cargo_type_id: UUID
    route_id: UUID
    weight: float
    volume: float
    amount: int
    source_id: UUID


class BuilkWorkCreate(BuilkWorkBase):
    data_time: int
    cargo_type_id: UUID
    route_id: UUID
    weight: float
    volume: float
    amount: int
    source_id: UUID


class BuilkWorkUpdate(BuilkWorkBase):
    data_time: int
    cargo_type_id: UUID
    route_id: UUID
    weight: float
    volume: float
    amount: int


class BuilkWorkData(BuilkWorkBase):
    data_time: int
    cargo_type_id: UUID
    route_id: UUID
    weight: float
    volume: float
    amount: int


class BuilkWorkInDBBase(BuilkWorkBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class BuilkWork(BuilkWorkInDBBase):
    pass


# Additional properties stored in DB
class BuilkWorkInDB(BuilkWorkInDBBase):
    pass
