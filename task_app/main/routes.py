from flask import Blueprint, render_template, flash
from task_app.models import Task
from flask_login import current_user, login_required
from datetime import date


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_today = (Task.query
                   .filter_by(user_id=current_user.id)
                   .filter_by(date_tasked=date.today()).all())
    if tasks_today:
        tasks_str = ", ".join(map(lambda t: t.title, tasks_today))
        flash(f"Today's tasks: {tasks_str}", "info")
    return render_template("home.html", tasks=tasks)

@main.route("/about")
def about():
    return render_template("about.html", pagetitle="About")

