from app import db, bcrypt
from app.models import User
from app.utils.tokens import TokenUtil
from flask import url_for

class PasswordService:

    @staticmethod
    def request_reset(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return None  # Vague on purpose

        token     = TokenUtil.generate_reset_token(user.email)
        reset_url = url_for("password.reset_password", token=token, _external=True)

        from celery_worker import send_reset_email
        send_reset_email.delay(user.email, reset_url)

        return None

    @staticmethod
    def reset_password(token, new_password):
        email = TokenUtil.verify_reset_token(token)
        if not email:
            return False, "The reset link is invalid or has expired."

        if len(new_password) < 6:
            return False, "Password must be at least 6 characters."

        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "User not found."

        user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        db.session.commit()
        return True, None
