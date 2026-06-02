from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.services.todo_service import TodoService
from app.services.category_service import CategoryService

todos = Blueprint("todos", __name__)

@todos.route("/")
@login_required
def index():
    page        = request.args.get("page", 1, type=int)
    category_id = request.args.get("category_id", None, type=int)
    pagination  = TodoService.get_paginated(current_user.id, page=page, category_id=category_id)
    all_cats    = CategoryService.get_all(current_user.id)
    return render_template("index.html",
        todos=pagination.items,
        pagination=pagination,
        categories=all_cats,
        selected_category=category_id
    )

@todos.route("/todos/add", methods=["POST"])
@login_required
def add_todo():
    title       = request.form.get("title")
    due_at_str  = request.form.get("due_at")
    category_id = request.form.get("category_id")

    todo, error = TodoService.create(current_user.id, title, due_at_str, category_id)

    if error:
        page       = request.args.get("page", 1, type=int)
        pagination = TodoService.get_paginated(current_user.id, page=page)
        all_cats   = CategoryService.get_all(current_user.id)
        return render_template("index.html",
            todos=pagination.items,
            pagination=pagination,
            categories=all_cats,
            error=error
        )

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
