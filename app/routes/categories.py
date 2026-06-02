from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.services.category_service import CategoryService

categories = Blueprint("categories", __name__)

@categories.route("/categories/add", methods=["POST"])
@login_required
def add_category():
    name = request.form.get("name")
    _, error = CategoryService.create(current_user.id, name)
    if error:
        all_cats = CategoryService.get_all(current_user.id)
        return render_template("categories.html", categories=all_cats, error=error)
    return redirect(url_for("categories.list_categories"))

@categories.route("/categories")
@login_required
def list_categories():
    all_cats = CategoryService.get_all(current_user.id)
    return render_template("categories.html", categories=all_cats)

@categories.route("/categories/<int:id>/delete", methods=["POST"])
@login_required
def delete_category(id):
    CategoryService.delete(id, current_user.id)
    return redirect(url_for("categories.list_categories"))
