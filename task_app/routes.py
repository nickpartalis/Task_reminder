from flask import render_template, url_for, flash, redirect, request
from task_app import app, db, bcrypt
from task_app.forms import RegistrationForm, LoginForm
from task_app.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required


dummy_tasks = [
    {
        "title": "Get a job",
        "content": "Gotta get a job",
        "date_created": "03/09/22",
        "date_tasked": ""
    },
    {
        "title": "Mom's birthday",
        "content": "",
        "date_created": "03/09/22",
        "date_tasked": "14/04"
    },
    {
        "title": "Do the dishes",
        "content": "Gotta do the dishes. Throw the trash out, too",
        "date_created": "04/09/22",
        "date_tasked": "04/09/22"
    },
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", tasks=dummy_tasks)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You are now logged in.", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("Login unsuccessful. Please check your email and password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")
