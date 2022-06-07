from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField


class OrderDeleteForm(FlaskForm):
    orderNumber = StringField("orderNumber")
