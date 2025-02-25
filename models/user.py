from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os


from . import Base, db_session
from .gift import Gift

JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-here')  # Make sure to set this in production

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    legal_first_name = Column(String(50))
    legal_last_name = Column(String(50))
    phone_number = Column(String(15))
    email = Column(String(100))
    password_hash = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    profile_picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    sent_gifts = relationship('Gift', back_populates='sent_from_user', foreign_keys='Gift.sent_from')
    received_gifts = relationship('Gift', back_populates='sent_to_user', foreign_keys='Gift.sent_to')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=86400):
        """Generate JWT token for the user
        
        Args:
            expires_in (int): Token expiration time in seconds (default: 24 hours)
        """
        return jwt.encode(
            {
                'user_id': str(self.uuid),
                'exp': datetime.utcnow() + timedelta(seconds=expires_in)
            },
            JWT_SECRET,
            algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return user
        
        Args:
            token (str): JWT token to verify
        Returns:
            User object or None if token is invalid
        """
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return User.get_by_uuid(data['user_id'])
        except:
            return None

    @classmethod
    def create(cls, first_name, last_name, phone_number, email, password):
        """Create a new user"""
        user = cls(
            legal_first_name=first_name,
            legal_last_name=last_name,
            phone_number=phone_number,
            email=email
        )
        user.password = password  # This will automatically hash the password
        db_session.add(user)
        db_session.commit()
        return user

    @classmethod
    def get_by_uuid(cls, uuid_str):
        """Get user by UUID"""
        return cls.query.filter_by(uuid=uuid_str).first()

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.legal_first_name} {self.legal_last_name}"