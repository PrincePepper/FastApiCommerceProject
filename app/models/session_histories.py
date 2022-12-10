# Sereda Semen
# 2022, 06.10
import time
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, func, null
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class SessionHistories(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    start_time = Column(Integer, nullable=False, default=int(time.time()),
                        server_default=func.extract('epoch', func.now()))
    end_time = Column(Integer, default=null, server_default=None)
