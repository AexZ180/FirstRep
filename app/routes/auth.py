from flask import Blueprint, render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password_raw = request.form.get("password", "").strip()

        if not email:
            return render_template("register.html", error="Please enter an email.")
        
        if not password_raw:
            return render_template("register.html", error="Please enter a password.")
        
        if len(password_raw) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.")
        
        if len(email) > 120:
            return render_template("register.html", error="Please enter an email shorter than 120 characters.")
        
        if len(password_raw) >255:
            return render_template("register.html", error="Please enter a password with length between 8-255 characters.")
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template("register.html", error="An account with this email already exists.")
        
        password_hash = generate_password_hash(password_raw)

        new_user = User(
            email = email,
            password_hash = password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return redirect(url_for("main.home"))
    return render_template("register.html")


@auth_bp.route("/login", methods =["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password_raw = request.form.get("password", "").strip()

        if not email:
            return render_template("login.html", error="Please input an email.")
        if not password_raw:
            return render_template("login.html", error="Please input a password.")
        
        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="No account associated with that email.")
        
        if not check_password_hash(user.password_hash, password_raw):
            return render_template("login.html", error = "Incorrect password.")
        
        session["user_id"] = user.id
        return redirect(url_for("main.home"))
    
    return render_template("login.html")