from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from . import Base, db_session

class Gift(Base):
    __tablename__ = 'gifts'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    sent_from = Column(Integer, ForeignKey('users.id'))
    sent_to = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    sent_from_user = relationship('User', back_populates='sent_gifts', foreign_keys=[sent_from])
    sent_to_user = relationship('User', back_populates='received_gifts', foreign_keys=[sent_to])

    @classmethod
    def create(cls, sent_from, sent_to, amount, asset_id=None):
        """Create a new gift"""
        gift = cls(
            sent_from=sent_from,
            sent_to=sent_to,
            amount=amount,
            asset_id=asset_id
        )
        db_session.add(gift)
        db_session.commit()
        return gift