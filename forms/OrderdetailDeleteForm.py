from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField


class OrderdetailDeleteForm(FlaskForm):
    orderNumber = StringField("orderNumber")
    productCode = StringField("productCode")
