from app import db
from app.models import Todo
from datetime import datetime

class TodoService:

    @staticmethod
    def get_paginated(user_id, page=1, per_page=10, category_id=None):
        query = Todo.query.filter_by(user_id=user_id)

        if category_id:
            query = query.filter_by(category_id=category_id)
        return query.order_by(Todo.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def create(user_id, title, due_at_str, category_id=None):
        title = title.strip() if title else ""

        if not title:
            return None, "Title cannot be empty."

        if len(title) > 200:
            return None, "Title is too long (max 200 characters)."

        existing = Todo.query.filter_by(user_id=user_id, title=title).first()
        if existing:
            return None, f"'{title}' already exists in your list."

        due_at = None
        if due_at_str:
            try:
                due_at = datetime.strptime(due_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                return None, "Invalid due date format."

        category_id = int(category_id) if category_id else None

        try:
            todo = Todo(title=title, user_id=user_id, due_at=due_at, category_id=category_id)
            db.session.add(todo)
            db.session.commit()
            return todo, None
        except Exception:
            db.session.rollback()
            return None, "Something went wrong. Please try again."

    @staticmethod
    def toggle(todo_id, user_id):
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            return None, "Todo not found."
        todo.done = not todo.done
        db.session.commit()
        return todo, None

    @staticmethod
    def delete(todo_id, user_id):
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            return None, "Todo not found."
        db.session.delete(todo)
        db.session.commit()
        return True, None
