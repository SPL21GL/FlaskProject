from flask import Flask, request
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
from forms.addProductForm import AddProductForm
from model.models import Product, Productline, db,Customer

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route("/products")
def products():
    #workaround für sesssion Autocomplete
    session : sqlalchemy.orm.scoping.scoped_session = db.session
    
    #alle products laden
    products = session.query(Product).order_by(Product.productCode).all()

    return render_template("products.html", products = products)


@products_blueprint.route("/products/add", methods=["GET","POST"])
def products_add():
    session : sqlalchemy.orm.scoping.scoped_session = db.session
    productlines = session.query(Productline).order_by(Productline.productLine).all()
    
    addProductForm = AddProductForm()

    if request.method == 'POST':
        
        if addProductForm.validate_on_submit():
            print("gültig")
            return render_template("products_add.html",productlines=productlines, form = addProductForm)
        else:
            raise "Fatal"
    else:
        return render_template("products_add.html",productlines=productlines,form = addProductForm)

