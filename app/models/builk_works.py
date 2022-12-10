# Sereda Semen
# 2022, 06.10


from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Float, Integer, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class BuilkWorks(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4,
                server_default=func.gen_random_uuid())
    data_time = Column(Integer, nullable=False)
    cargo_type_id = Column(UUID(as_uuid=True), ForeignKey("cargo_types.id"))
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"))
    weight = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"))
