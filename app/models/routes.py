# Sereda Semen
# 2022, 06.10


from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Routes(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    name = Column(String(64), nullable=False)
    from_id = Column(UUID(as_uuid=True), ForeignKey("road_points.id"), nullable=False)
    to_id = Column(UUID(as_uuid=True), ForeignKey("road_points.id"), nullable=False)
    __table_args__ = (UniqueConstraint('from_id', 'to_id', name='idx_from_id_to_id'),)
