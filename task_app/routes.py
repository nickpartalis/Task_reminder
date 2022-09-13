from flask import render_template, url_for, flash, redirect, request, abort
from task_app import app, db, bcrypt
from task_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, TaskCreateForm, TaskUpdateForm
from task_app.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", tasks=tasks)

@app.route("/about")
def about():
    return render_template("about.html", pagetitle="About")

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
    return render_template("register.html", form=form, pagetitle="Register")

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
    return render_template("login.html", form=form, pagetitle="Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): 
        if form.username.data != current_user.username or form.email.data != current_user.email:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account information have been updated.", "success")
            return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form, pagetitle="My Account")


@app.route("/task/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskCreateForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, 
                    date_tasked=form.date_tasked.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Your task has been created.", "success")
        return redirect(url_for("home"))
    return render_template("create_task.html", form=form, legend="Create Task", pagetitle="Create Task")

@app.route("/task/<int:task_id>", methods=["GET", "POST"])
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    return render_template("task.html", task=task)

@app.route("/task/<int:task_id>/update", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    form = TaskUpdateForm()
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        task.date_tasked = form.date_tasked.data
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("home", task_id=task.id))
    elif request.method == "GET":
        form.title.data = task.title
        form.content.data = task.content
    return render_template("create_task.html", form=form, legend="Update Task", pagetitle="Update Task")

@app.route("/task/<int:task_id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("home"))
