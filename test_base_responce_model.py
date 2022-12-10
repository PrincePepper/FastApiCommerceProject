from typing import TypeVar, Generic, Optional
from uuid import UUID

from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """ Твоя базовая модель"""
    id: int=5


ModelClass = TypeVar('ModelClass', bound=BaseResponseModel)


class UserCreate(Generic[ModelClass]):
    email: str
    password: str


class BaseResponse(BaseModel):
    """Твой базовый респонсу"""
    status: int = 0
    message: str = "ok"
    data: list


a = UserCreate()
b = BaseResponse(data=[UserCreate[BaseResponseModel]])
print(b.data[0].id)
