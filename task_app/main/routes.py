from flask import Blueprint
from flask import render_template
from task_app.models import Task
from flask_login import current_user, login_required


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", tasks=tasks)

@main.route("/about")
def about():
    return render_template("about.html", pagetitle="About")

