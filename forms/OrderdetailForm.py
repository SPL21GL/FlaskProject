from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.fields import DecimalField, SelectField


class OrderdetailForm(FlaskForm):
    orderNumber = StringField("orderNumber")
    productCode = SelectField("productCode")
    quantityOrdered = DecimalField("quantityOrdered")
    priceEach = DecimalField("priceEach")
    orderLineNumber = DecimalField("orderLineNumber")
