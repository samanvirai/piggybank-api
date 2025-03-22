from models import User, db_session
from werkzeug.security import check_password_hash

class AuthService:
  @staticmethod
  def sign_up(first_name, last_name, phone_number, email, password):
    user = User.create(first_name, last_name, phone_number, email, password)
    return user

  @staticmethod
  def login(email, password):
    user = User.get_by_email(email)
    if user and user.verify_password(password):
      return user.generate_auth_token()
    return None
  
  