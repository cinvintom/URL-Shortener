from sqlalchemy import Column, Integer, DateTime, String, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from app.db.base_class import Base


class UrlType(PyEnum):
    RANDOM = "RANDOM"
    CUSTOM = "CUSTOM"


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class UrlMapping(BaseModel):
    __tablename__ = "url_mappings"

    original_url = Column(String(2048), index=True)
    short_url = Column(String(10), index=True, unique=True)
    url_type = Column(SQLAlchemyEnum(UrlType), default=UrlType.RANDOM)
