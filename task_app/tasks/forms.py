from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import date

class TaskFormMixin(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Description (Optional)")
    date_tasked = DateField("Date Tasked (Optional)", format="%Y-%m-%d", validators=[Optional()])

    def validate_date_tasked(self, date_tasked):
        if date_tasked.data < date.today():
            raise ValidationError("The scheduled date cannot be in the past!")
       

class TaskCreateForm(TaskFormMixin):
    submit = SubmitField("Create Task")


class TaskUpdateForm(TaskFormMixin):
    submit = SubmitField("Update Task")