from flask import Flask, redirect, request
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
            #hier in db einfügen
            newProduct = Product()

            newProduct.productCode = addProductForm.productCode.data
            newProduct.productName = addProductForm.productName.data
            newProduct.productLine = addProductForm.productLine.data
            newProduct.productScale = addProductForm.productScale.data
            newProduct.productVendor = addProductForm.productVendor.data
            newProduct.productDescription = addProductForm.productDescription.data
            newProduct.quantityInStock = addProductForm.quantityInStock.data
            newProduct.buyPrice = addProductForm.buyPrice.data
            newProduct.MSRP = addProductForm.MSRP.data

            db.session.add(newProduct)
            db.session.commit()

            return redirect("/products")
        else:
            return render_template("products_add.html",productlines=productlines,form = addProductForm)
    else:
        return render_template("products_add.html",productlines=productlines,form = addProductForm)

