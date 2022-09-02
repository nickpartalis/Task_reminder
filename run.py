from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "1473212a377d56db0c3506adee1348e8"

dummy_tasks = [
    {
        "title": "Get a job",
        "content": "Gotta get a job",
        "date_created": "03/09/2022",
        "date_tasked": ""
    },
    {
        "title": "Mom's birthday",
        "content": "",
        "date_created": "03/09/2022",
        "date_tasked": "14/04"
    },
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", tasks=dummy_tasks)

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

if __name__ == "__main__":
    app.run(debug=True)