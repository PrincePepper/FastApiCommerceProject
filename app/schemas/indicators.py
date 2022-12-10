from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel, Json


# Shared properties
class IndicatorBase(BaseModel):
    name: str
    alias: str
    diagram_type: int
    properties: Optional[Dict]
    text_sql: str = None


class IndicatorCreate(IndicatorBase):
    name: str
    alias: str
    diagram_type: int
    properties: Json
    text_sql: str


class IndicatorUpdate(IndicatorBase):
    name: str = None
    alias: str = None
    diagram_type: int = None
    properties: Json = None
    text_sql: str = None


class IndicatorAllInformation(BaseModel):
    indicator_id: UUID
    last_update: int
    labels: list
    datasets: list
    title: str


class IndicatorFullInformation(BaseModel):
    screen_number: int
    instance_id: UUID
    instance_properties: Optional[Dict]
    diagram_type: int
    indicator_id: UUID
    name: str
    indicator_properties: Optional[Dict]


class IndicatorInDBBase(IndicatorBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Indicator(IndicatorInDBBase):
    pass


# Additional properties stored in DB
class IndicatorInDB(IndicatorInDBBase):
    pass


# INDICATOR INSTANCE
#
# Shared properties
class IndicatorInstanceBase(BaseModel):
    indicators_access_id: UUID
    screen_number: int
    properties: Json


class IndicatorInstanceCreate(IndicatorInstanceBase):
    indicators_access_id: UUID
    screen_number: int
    properties: Json


class IndicatorInstanceChange(BaseModel):
    last_update: int
    user_id: UUID
    screen: int


class IndicatorInstanceUpdate(IndicatorInstanceBase):
    pass


class IndicatorInstanceInDBBase(IndicatorInstanceBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class IndicatorInstance(IndicatorInstanceInDBBase):
    pass


# Additional properties stored in DB
class IndicatorInstanceInDB(IndicatorInstanceInDBBase):
    pass


# INDICATOR ACCESS
#
# Shared properties
class IndicatorAccessBase(BaseModel):
    indicator_id: UUID
    user_id: UUID = None
    is_active: bool = True


class IndicatorsAccessInformation(BaseModel):
    indicators_access_id: UUID
    indicator_id: UUID
    indicators_name: str
    diagram_type: str


class IndicatorAccessCreate(IndicatorAccessBase):
    indicator_id: UUID
    user_id: UUID
    is_active: bool


class IndicatorAccessUpdate(IndicatorAccessBase):
    indicator_id: UUID
    user_id: UUID
    is_active: bool


class IndicatorAccessUpdateStatus(BaseModel):
    indicator_id: UUID
    users: dict


class IndicatorAccessInDBBase(IndicatorAccessBase):
    id: UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class IndicatorAccess(IndicatorAccessInDBBase):
    pass


# Additional properties stored in DB
class IndicatorAccessInDB(IndicatorAccessInDBBase):
    pass
