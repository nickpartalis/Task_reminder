from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired

class TaskFormMixin(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content")
    date_tasked = DateField("Date Tasked")
    

class TaskCreateForm(TaskFormMixin):
    submit = SubmitField("Create Task")


class TaskUpdateForm(TaskFormMixin):
    submit = SubmitField("Update Task")