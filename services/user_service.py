from models import User
from typing import Optional

class UserService:    
    @staticmethod
    def get_user_by_token(token: str) -> Optional[User]:
        user = User.verify_auth_token(token)
        if not user:
            return None
        return user
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        return User.get_by_email(email)