# Sereda Semen
# 2022, 06.10


from uuid import uuid4

from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class CargoTypes(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    name = Column(String(128), index=True, nullable=False, default='', server_default='')
