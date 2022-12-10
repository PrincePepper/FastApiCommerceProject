from uuid import UUID

from pydantic import BaseModel


# Shared properties
class CargoTypeBase(BaseModel):
    name: str
    id: UUID


class CargoTypeCreate(CargoTypeBase):
    name: str
    id: UUID


class CargoTypeUpdate(CargoTypeBase):
    name: str
    id: UUID


class CargoTypeInDBBase(CargoTypeBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class CargoType(CargoTypeInDBBase):
    pass


# Additional properties stored in DB
class CargoTypeInDB(CargoTypeInDBBase):
    pass
