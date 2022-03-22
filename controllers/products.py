from flask import Flask, redirect, request, flash
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
from forms.ProductDeleteForm import ProductDeleteForm
from forms.ProductForm import ProductForm
from model.models import Product, Productline, db,Customer

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route("/products")
def products():
    #workaround für sesssion Autocomplete
    session : sqlalchemy.orm.scoping.scoped_session = db.session
    
    #alle products laden
    products = session.query(Product).order_by(Product.productCode).all()

    return render_template("products/products.html", products = products)


@products_blueprint.route("/products/add", methods=["GET","POST"])
def products_add():
    session : sqlalchemy.orm.scoping.scoped_session = db.session
    
    addProductForm = ProductForm()
    
    productlines = session.query(Productline).order_by(Productline.productLine).all()
    product_line_list = [(p.productLine, p.productLine) for p in productlines]
    addProductForm.productLine.choices = product_line_list

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
            return render_template("products/products_add.html",productlines=productlines,form = addProductForm)
    else:
        return render_template("products/products_add.html",productlines=productlines,form = addProductForm)

@products_blueprint.route("/products/edit", methods=["GET","POST"])
def products_edit():
    session : sqlalchemy.orm.scoping.scoped_session = db.session

    editProductForm = ProductForm()

    productlines = session.query(Productline).order_by(Productline.productLine).all()
    product_line_list = [(p.productLine, p.productLine) for p in productlines]
    editProductForm.productLine.choices = product_line_list

    productCode = request.args["productCode"]

    #item laden (wie kann man einen datensatz lesen)
    product_to_edit = session.query(Product).filter(Product.productCode == productCode).first()
    
    if request.method == "POST":
        if editProductForm.validate_on_submit():
            productCode = editProductForm.productCode.data
            product_to_edit = db.session.query(Product).filter(Product.productCode == productCode).first()
            
            product_to_edit.productName = editProductForm.productName.data
            product_to_edit.productLine = editProductForm.productLine.data
            product_to_edit.productScale = editProductForm.productScale.data
            product_to_edit.productVendor = editProductForm.productVendor.data
            product_to_edit.productDescription = editProductForm.productDescription.data
            product_to_edit.quantityInStock = editProductForm.quantityInStock.data
            product_to_edit.buyPrice = editProductForm.buyPrice.data
            product_to_edit.MSRP = editProductForm.MSRP.data

            db.session.commit()
        return redirect("/products")
    else:
        editProductForm.productCode.data = product_to_edit.productCode
        editProductForm.productName.data = product_to_edit.productName
        editProductForm.productLine.data = product_to_edit.productLine
        editProductForm.productScale.data = product_to_edit.productScale
        editProductForm.productVendor.data = product_to_edit.productVendor
        editProductForm.productDescription.data = product_to_edit.productDescription
        editProductForm.quantityInStock.data = product_to_edit.quantityInStock
        editProductForm.buyPrice.data = product_to_edit.buyPrice
        editProductForm.MSRP.data = product_to_edit.MSRP

        return render_template("products/products_edit.html",productlines=productlines,form = editProductForm)

@products_blueprint.route("/products/delete", methods=["post"])
def deleteProduct():
    deleteItemFormObj = ProductDeleteForm()
    if deleteItemFormObj.validate_on_submit():

        productCodeToDelete = deleteItemFormObj.productCode.data
        productToDelete = db.session.query(Product).filter(Product.productCode == productCodeToDelete)
        productToDelete.delete()
        
        db.session.commit()
    else:
        print("Fatal Error")
    
    flash(f"Product with id {productCodeToDelete} has been deleted")    

    return redirect("/products")