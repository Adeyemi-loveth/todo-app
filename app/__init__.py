from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os
import time

db      = SQLAlchemy()
login   = LoginManager()
mail    = Mail()
bcrypt  = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SECRET_KEY"]              = os.environ["SECRET_KEY"]
    app.config["MAIL_SERVER"]             = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"]               = int(os.environ.get("MAIL_PORT", 465))
    app.config["MAIL_USE_TLS"]            = False
    app.config["MAIL_USE_SSL"]            = True
    app.config["MAIL_USERNAME"]           = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"]           = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"]     = os.environ.get("MAIL_USERNAME")

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login.login_view    = "auth.login"
    login.login_message = "Please log in to access your todos."

    from app.models import User
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from .routes.auth       import auth
        from .routes.todos      import todos
        from .routes.categories import categories
        from .routes.password   import password
        app.register_blueprint(auth)
        app.register_blueprint(todos)
        app.register_blueprint(categories)
        app.register_blueprint(password)

        for attempt in range(10):
            try:
                db.create_all()
                print("Database tables ready.")
                break
            except Exception as e:
                print(f"Database not ready (attempt {attempt + 1}/10): {e}")
                time.sleep(3)

    return app
