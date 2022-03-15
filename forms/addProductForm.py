from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import BooleanField, StringField, TextAreaField
from wtforms.fields import DecimalField
from wtforms import validators

class AddProductForm(FlaskForm):
    productCode = StringField("productCode")
    productName = StringField("productName")
    productLine = StringField("productLine")
    productScale = StringField("productScale")
    productVendor = StringField("productVendor")
    productDescription = TextAreaField("productDescription")
    quantityInStock = DecimalField("quantityInStock")
    buyPrice = DecimalField("buyPrice")
    MSRP = DecimalField("MSRP")