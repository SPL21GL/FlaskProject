from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import BooleanField, StringField, TextAreaField
from wtforms.fields import DecimalField, SelectField
from wtforms import validators

class ProductForm(FlaskForm):
    productCode = StringField("productCode",[validators.InputRequired()])
    productName = StringField("productName")
    productLine =  SelectField("productLine") #StringField("productLine")

    productScale = StringField("productScale")
    productVendor = StringField("productVendor")
    productDescription = TextAreaField("productDescription")
    quantityInStock = DecimalField("quantityInStock")
    buyPrice = DecimalField("buyPrice")
    MSRP = DecimalField("MSRP")