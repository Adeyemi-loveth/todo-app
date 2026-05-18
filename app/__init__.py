from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["CELERY_BROKER_URL"] = os.environ["REDIS_URL"]

    db.init_app(app)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
        db.create_all()

    return app
