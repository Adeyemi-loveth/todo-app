from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import os

db      = SQLAlchemy()
login   = LoginManager()
mail    = Mail()
bcrypt  = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SECRET_KEY"]              = os.environ["SECRET_KEY"]
    app.config["MAIL_SERVER"]             = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"]               = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"]            = True
    app.config["MAIL_USERNAME"]           = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"]           = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"]     = os.environ.get("MAIL_USERNAME")

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    login.login_view    = "auth.login"
    login.login_message = "Please log in to access your todos."

   
    from app.models import User
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from .routes.auth  import auth
        from .routes.todos import todos
        app.register_blueprint(auth)
        app.register_blueprint(todos)
        db.create_all()

    return app
