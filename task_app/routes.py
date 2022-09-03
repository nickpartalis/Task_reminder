from flask import render_template, url_for, flash, redirect
from task_app import app
from task_app.forms import RegistrationForm, LoginForm


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("You are now logged in.", "success")
        return redirect(url_for("home"))
    return render_template("login.html", form=form)
