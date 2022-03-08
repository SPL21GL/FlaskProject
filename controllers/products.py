from flask import Flask
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
from model.models import Product, db,Customer

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route("/products")
def products():
    #workaround für sesssion Autocomplete
    session : sqlalchemy.orm.scoping.scoped_session = db.session
    
    #alle products laden
    products = session.query(Product).all()

    return render_template("products.html", products = products)