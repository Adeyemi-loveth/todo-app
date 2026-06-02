from flask import Blueprint, render_template, request, redirect, url_for
from app.services.password_service import PasswordService

password = Blueprint("password", __name__)

@password.route("/reset-password", methods=["GET", "POST"])
def request_reset():
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        if not email:
            return render_template("reset_request.html", error="Email is required.")
        
        PasswordService.request_reset(email)
        return render_template("reset_request.html",
            message="If that email exists, a reset link has been sent. Check your inbox."
        )

    return render_template("reset_request.html")


@password.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    
    if request.method == "POST":
        new_password = request.form.get("password", "")

        success, error = PasswordService.reset_password(token, new_password)

        if error:
            return render_template("reset_password.html", token=token, error=error)

        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", token=token)
