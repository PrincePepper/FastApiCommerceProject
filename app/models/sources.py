# Sereda Semen
# 2022, 06.10
import time
from uuid import uuid4

from sqlalchemy import Column, String, JSON, func, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Sources(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    name = Column(String(64))
    address = Column(String(64))
    last_update = Column(Integer, default=int(time.time()),
                         server_default=func.extract('epoch', func.now()))
    properties = Column(JSON)


class SourcesDependencies(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4,
                server_default=func.gen_random_uuid())
    indicator_id = Column(UUID(as_uuid=True), ForeignKey('indicators.id'), nullable=False)
    source_id = Column(UUID(as_uuid=True), ForeignKey('sources.id'), nullable=False)
