# Sereda Semen
# 2022, 06.10


from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, func, Text, Boolean, Integer, JSON, \
    UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Indicators(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    name = Column(String(64), index=True, nullable=False)
    alias = Column(String(30), nullable=False)
    diagram_type = Column(Integer, nullable=False)
    properties = Column(JSON, nullable=False)
    text_sql = Column(Text)


class IndicatorsAccess(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    indicator_id = Column('indicator_id', UUID(as_uuid=True), ForeignKey('indicators.id'))
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    is_active = Column(Boolean(), nullable=False, default=True, server_default='true', index=True)
    __table_args__ = (UniqueConstraint('indicator_id', 'user_id', name='idx_indicator_id_user_id'),)


# indicator_access_table = Table(
#     'indicators_access',
#     Base.metadata,
#     Column('id', UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid4,
#            server_default=func.gen_random_uuid()),
#     Column('indicator_id', UUID(as_uuid=True), ForeignKey('indicators.id'), nullable=False),
#     Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), nullable=False),
#     Column('is_active', Boolean(), index=True, nullable=False, default=True, server_default='true'))


class IndicatorInstance(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid4,
                server_default=func.gen_random_uuid())
    indicators_access_id = Column(UUID(as_uuid=True), ForeignKey('indicators_access.id'),
                                  index=True, nullable=False)
    screen_number = Column(Integer, nullable=False)
    properties = Column(JSON, nullable=False)
