from .base import BaseRepository
from models.gift import Gift
from sqlalchemy.orm import joinedload

class GiftRepository(BaseRepository):
    def all(self, **filters):
        return self.session.query(Gift).filter_by(**filters).all()

    def get_gift_sent_count(self, user_id):
        """Get count of gifts sent by a user"""
        sent_count = self.session.query(Gift).filter_by(sent_from=user_id).count()
        return sent_count
    
    def get_gift_received_count(self, user_id):
        """Get count of gifts received by a user"""
        received_count = self.session.query(Gift).filter_by(sent_to=user_id).count()
        return received_count