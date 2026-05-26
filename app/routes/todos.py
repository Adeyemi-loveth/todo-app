from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.services.todo_service import TodoService

todos = Blueprint("todos", __name__)

@todos.route("/")
@login_required       
def index():
    all_todos, _ = TodoService.get_all(current_user.id), None
    all_todos = TodoService.get_all(current_user.id)
    return render_template("index.html", todos=all_todos)

@todos.route("/todos/add", methods=["POST"])
@login_required
def add_todo():
    title      = request.form.get("title")
    due_at_str = request.form.get("due_at")

    todo, error = TodoService.create(current_user.id, title, due_at_str)

    if error:
        all_todos = TodoService.get_all(current_user.id)
        return render_template("index.html", todos=all_todos, error=error)

    return redirect(url_for("todos.index"))

@todos.route("/todos/<int:id>/toggle", methods=["POST"])
@login_required
def toggle_todo(id):
    TodoService.toggle(id, current_user.id)
    return redirect(url_for("todos.index"))

@todos.route("/todos/<int:id>/delete", methods=["POST"])
@login_required
def delete_todo(id):
    TodoService.delete(id, current_user.id)
    return redirect(url_for("todos.index"))
