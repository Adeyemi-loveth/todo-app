from app import db
from app.models import Category

class CategoryService:

    @staticmethod
    def get_all(user_id):
        return Category.query.filter_by(user_id=user_id).order_by(Category.name).all()

    @staticmethod
    def create(user_id, name):
        name = name.strip() if name else ""

        if not name:
            return None, "Category name cannot be empty."

        if len(name) > 100:
            return None, "Category name is too long (max 100 characters)."

        existing = Category.query.filter_by(user_id=user_id, name=name).first()
        if existing:
            return None, f"Category '{name}' already exists."

        try:
            category = Category(name=name, user_id=user_id)
            db.session.add(category)
            db.session.commit()
            return category, None
        except Exception:
            db.session.rollback()
            return None, "Something went wrong. Please try again."

    @staticmethod
    def delete(category_id, user_id):
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
        if not category:
            return None, "Category not found."
        db.session.delete(category)
        db.session.commit()
        return True, None
