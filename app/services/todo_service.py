from app import db
from app.models import Todo
from datetime import datetime

class TodoService:
    @staticmethod
    def get_all(user_id):
        return Todo.query.filter_by(user_id=user_id).order_by(Todo.created_at.desc()).all()
    
    @staticmethod
    def create(user_id, title, due_at_str):
        title = title.strip() if title else ""
        if not title:
            return None, "Title cannot be empty."
        if len(title) > 200:
            return None, "Title is too long (max 200 characters)."
        
        existing = Todo.query.filter_by(user_id=user_id, title=title).first()
        if existing:
            return None, f" '{title}' already exists in your list."
        
        due_at = None
        if due_at_str:
            try:
                due_at = datetime.strptime(due_at_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                return None, "Invalid due date format."
            
        try:
            todo = Todo(title=title, user_id=user_id, due_at=due_at)
            db.session.add(todo)
            db.session.commit()
            return todo, None
        except Exception:
            db.session.roolback()
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

        


