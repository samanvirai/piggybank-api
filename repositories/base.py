from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class AbstractRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, id):
        pass

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)

    def remove(self, entity):
        self.session.delete(entity)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback() 