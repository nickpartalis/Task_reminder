from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from task_app import db, bcrypt, mail
from task_app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                  RequestResetForm, ResetPasswordForm)
from task_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os


users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, pagetitle="Register")

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You are now logged in.", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        flash("Login unsuccessful. Please check your email and password.", "danger")
    return render_template("login.html", form=form, pagetitle="Login")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): 
        if form.username.data != current_user.username or form.email.data != current_user.email:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account information have been updated.", "success")
            return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form, pagetitle="My Account")

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("[Task Reminder] Reset Password", 
                  sender=os.environ.get("MAIL_USERNAME"), recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email.
"""
    mail.send(msg)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Recovery email sent. Check your inbox for the password reset link.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form=form, pagetitle="Reset Password")

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Your password reset token is invalid or expired.", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pwd
        db.session.commit()
        flash("Your password has been updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", form=form, pagetitle="Reset Password")
