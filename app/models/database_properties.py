# Sereda Semen
# 2022, 06.10


from sqlalchemy import Column, String

from app.db.base_class import Base


class DatabaseProperties(Base):
    version = Column(String(64), primary_key=True, nullable=False)
