from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField
from wtforms.fields import SelectField
from wtforms import validators, HiddenField

choices = [("Shipped", "Shipped"), ("Resolved", "Resolved"), ("Cancelled", "Cancelled"),
           ("On Hold", "On Hold"), ("Disputed", "Disputed"), ("In Process", "In Process")]


class OrderForm(FlaskForm):
    orderNumber = HiddenField("orderNumber")
    orderDate = DateField("orderDate", [validators.InputRequired()])
    requiredDate = DateField("orderDate", [validators.InputRequired()])
    shippedDate = DateField("orderDate", [validators.InputRequired()])
    status = SelectField("status", choices=choices)
    comments = TextAreaField("comments")
    customer = SelectField("customer")
