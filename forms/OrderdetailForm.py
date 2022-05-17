from random import choices
from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import BooleanField, StringField, TextAreaField
from wtforms.fields import DecimalField, SelectField
from wtforms import validators, HiddenField


class OrderdetailForm(FlaskForm):
    orderNumber = SelectField("orderNumber")
    productCode = SelectField("productCode")
    quantityOrdered = DecimalField("quantityOrdered")
    priceEach = DecimalField("priceEach")
    orderLineNumber = DecimalField("orderLineNumber")
