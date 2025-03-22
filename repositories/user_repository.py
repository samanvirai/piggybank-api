from .base import BaseRepository
from models.user import User
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from typing import Callable

class UserRepository(BaseRepository):
    def add(self, user: User):
        self.session.add(user)
        return user

    def get(self, uuid):
        return self.session.query(User).filter(User.uuid == uuid).first()
    
    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()
    
    def get_active_users(self):
        return self.session.query(User).filter(User.is_active == True).all()

    def get_by_uuid(self, uuid_str):
        return self.session.query(User).filter_by(uuid=uuid_str).first()

    def all(self, **filters):
        return self.session.query(User).filter_by(**filters).all()

class UnitOfWork(AbstractContextManager):
    def __init__(self, session_factory: Callable[..., Session]):
        self.session_factory = session_factory
        
    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:  # An exception occurred
            self.rollback()
        self.session.close()
        
    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback() 