from repositories.user_repository import UserRepository
from repositories.gift_repository import GiftRepository
from repositories.asset_repository import AssetRepository
from models import db_session

class UnitOfWork:
    def __init__(self):
        self.session = db_session
        self.users = UserRepository(self.session)
        self.gifts = GiftRepository(self.session)
        self.assets = AssetRepository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.remove() 