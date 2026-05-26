from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import AuthService

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name     = request.form.get("name")
        email    = request.form.get("email")
        password = request.form.get("password")

        user, error = AuthService.signup(name, email, password)

        if error:
            return render_template("signup.html", error=error)

        login_user(user)
        return redirect(url_for("todos.index"))

    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email")
        password = request.form.get("password")

        user, error = AuthService.login(email, password)

        if error:
            return render_template("login.html", error=error)

        login_user(user)
        return redirect(url_for("todos.index"))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
