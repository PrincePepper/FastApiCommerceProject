# Sereda Semen
# 2022, 06.10
import time
from uuid import uuid4

from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Users(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4,
                server_default=func.gen_random_uuid())
    email = Column(String(64), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    is_admin = Column(Boolean(), default=False, server_default='false')
    is_active = Column(Boolean(), default=False, server_default='false')
    created_at = Column(Integer, default=int(time.time()),
                        server_default=func.extract('epoch', func.now()))
    password = Column(String, nullable=False)
    name = Column(String(128), nullable=False)
    country_code = Column(Integer, default=7, server_default='7')
