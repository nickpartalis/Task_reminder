from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from task_app import db
from task_app.tasks.forms import TaskCreateForm, TaskUpdateForm
from task_app.models import Task
from flask_login import current_user, login_required


tasks = Blueprint("tasks", __name__)

@tasks.route("/task/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskCreateForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, 
                    date_tasked=form.date_tasked.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Your task has been created.", "success")
        return redirect(url_for("main.home"))
    return render_template("create_task.html", form=form, legend="Create Task", pagetitle="Create Task")

@tasks.route("/task/<int:task_id>", methods=["GET", "POST"])
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    return render_template("task.html", task=task)

@tasks.route("/task/<int:task_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("main.home", task_id=task.id))
    elif request.method == "GET":
        form.title.data = task.title
        form.content.data = task.content
        form.date_tasked.data = task.date_tasked
    return render_template("create_task.html", form=form, legend="Update Task", pagetitle="Update Task")

@tasks.route("/task/<int:task_id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("main.home"))
