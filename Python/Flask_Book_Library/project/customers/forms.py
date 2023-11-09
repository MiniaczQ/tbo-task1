# Form imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from ..validators.no_html import NoHtml


# Flask forms (wtforms) allow you to easily create forms in this format:
class CreateCustomer(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), NoHtml()])
    city = StringField("City", validators=[DataRequired(), NoHtml()])
    age = IntegerField("Age", validators=[DataRequired()])
    submit = SubmitField("Create Customer")


class EditCustomer(FlaskForm):
    name = StringField("Name", validators=[NoHtml()])
    city = StringField("City", validators=[NoHtml()])
    age = IntegerField("Age")
