from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base, db_session

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    name = Column(String)
    ticker = Column(String)
    logo_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    def create(cls, name, ticker=None, logo_url=None):
        """Create a new asset"""
        asset = cls(
            name=name,
            ticker=ticker,
            logo_url=logo_url,
        )
        db_session.add(asset)
        db_session.commit()
        return asset