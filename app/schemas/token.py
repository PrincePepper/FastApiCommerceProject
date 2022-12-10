from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
