from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Get database URL from environment variable, with a default for local development
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/mydatabase')

engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from .user import User
from .gift import Gift
from .asset import Asset

__all__ = ['User', 'Gift', 'Asset', 'db_session', 'Base'] 