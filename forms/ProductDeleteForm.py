from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms import validators


class ProductDeleteForm(FlaskForm):
    productCode = StringField("productCode", [validators.InputRequired()])
