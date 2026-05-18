from flask import Blueprint, request, redirect, url_for, render_template
from . import db
from .models import Todo
from celery_worker import send_reminder

main = Blueprint("main", __name__)

@main.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@main.route("/todos/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
        send_reminder.delay(todo.title)
    return redirect(url_for("main.index"))

@main.route("/todos/<int:id>/toggle", methods=["POST"])
def toggle_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/todos/<int:id>/delete", methods=["POST"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.index"))
