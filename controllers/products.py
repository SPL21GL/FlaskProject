from flask import Flask
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
from model.models import db,Customer

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route("/products")
def products():

    return render_template("products.html")