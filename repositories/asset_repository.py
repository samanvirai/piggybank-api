from .base import BaseRepository
from models.asset import Asset

class AssetRepository(BaseRepository):
    def all(self, **filters):
        return self.session.query(Asset).filter_by(**filters).all()

    def get_by_id(self, id):
        return self.session.query(Asset).filter_by(id=id).first()