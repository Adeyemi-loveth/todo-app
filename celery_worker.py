import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery import Celery
from celery.schedules import crontab

def make_celery():
    app = Celery(
        "tasks",
        broker=os.environ["REDIS_URL"],
        include=["celery_worker"]
    )
    app.conf.beat_schedule = {
        "check-due-todos-every-minute": {
            "task": "celery_worker.check_due_todos",
            "schedule": crontab(minute="*"),
        }
    }
    return app

celery = make_celery()

@celery.task
def send_reset_email(user_email, reset_url):
    """
    Sends password reset email in the background.
    Flask queues this and responds immediately —
    user doesn't wait for Gmail to respond.
    """
    from app import create_app
    from app.utils.email import EmailUtil

    flask_app = create_app()
    with flask_app.app_context():
        try:
            EmailUtil.send_password_reset(user_email, reset_url)
            print(f"[RESET EMAIL] Sent to {user_email}")
        except Exception as e:
            print(f"[RESET EMAIL] Failed to send to {user_email}: {e}")

@celery.task
def check_due_todos():
    from datetime import datetime, timedelta
    from app import create_app, db
    from app.models import Todo, User
    from app.utils.email import EmailUtil

    flask_app = create_app()

    with flask_app.app_context():
        now  = datetime.utcnow()
        soon = now + timedelta(minutes=30)

        print(f"[REMINDER CHECK] Running at {now}")

        due_todos = Todo.query.filter(
            Todo.due_at  >= now,
            Todo.due_at  <= soon,
            Todo.done    == False,
            Todo.reminded == False
        ).all()

        print(f"[REMINDER CHECK] Found {len(due_todos)} todos due soon")

        for todo in due_todos:
            user = User.query.get(todo.user_id)
            if user:
                print(f"[REMINDER CHECK] Sending to {user.email} for todo '{todo.title}'")
                try:
                    EmailUtil.send_reminder(
                        user.email,
                        user.name,
                        todo.title,
                        todo.due_at
                    )
                    todo.reminded = True
                    db.session.commit()
                    print(f"[REMINDER CHECK] Success!")
                except Exception as e:
                    print(f"[REMINDER CHECK] FAILED: {e}")
                    import traceback
                    traceback.print_exc()
