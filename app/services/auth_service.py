from app import db, bcrypt
from app.models import User

class AuthService:
    @staticmethod
    def signup(name, email, password):
        if not name or not email or not password:
            return None, "All fields are required."
        if len(password) < 6:
            return None, "Password must be at least 6 characters."
        if User.query.filter_by(email=email).first():
            return None, "An account with this email already exists."
        
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(name=name, email=email, password_hash=password_hash)

        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception:
            db.session.rollback()
            return None, "Something went wrong. Please try again."
        
    @staticmethod
    def login(email, password):
        if not email or not password:
            return None, "All fields are required."
        
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None, "Invalid email or passowrd."
        
        return user, None
        
