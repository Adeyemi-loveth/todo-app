from flask_mail import Message
from app import mail

class EmailUtil:

    @staticmethod
    def send_reminder(user_email, user_name, todo_title, due_at):
        msg = Message(
            subject="Reminder: Task due soon!",
            recipients=[user_email]
        )
        msg.body = (
            f"Hi {user_name},\n\n"
            f"Your task '{todo_title}' is due at {due_at.strftime('%Y-%m-%d %H:%M')}.\n"
            f"Don't forget to complete it!\n\n"
            f"- Your Todo App"
        )
        mail.send(msg)
