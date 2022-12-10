# Sereda Semen
# 2022, 00.00
from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    detail: str


class DefaultBodyResponse(BaseModel):
    status: int = 0
    message: Optional[str] = "ok"
    data: BaseModel = None


class UserCreate(BaseModel):
    email: str
    password: str


aaa = DefaultBodyResponse
print(aaa)
