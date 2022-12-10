from pydantic import BaseModel


class DatabaseProperties(BaseModel):
    version: str

    class Config:
        orm_mode = True


class DatabaseGetInfo(BaseModel):
    host: str
    port: str
    username: str
    password: str
    db: str
    list_db: list


class DatabaseInfo(BaseModel):
    host: str
    port: str
    username: str
    password: str
    db: str
