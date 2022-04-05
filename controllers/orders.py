from flask import Flask, redirect, request, flash
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
import flask_sqlalchemy
from forms.OrderForm import OrderForm
from model.models import Customer, Order, db

orders_blueprint = Blueprint('orders_blueprint', __name__)


@orders_blueprint.route("/orders")
def orders():
    # workaround für sesssion Autocomplete
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    orders = session.query(Order).order_by(Order.orderNumber).all()

    return render_template("orders/orders.html", orders=orders)


@orders_blueprint.route("/orders/add", methods=["GET", "POST"])
def orders_add():
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    add_order_form = OrderForm()

    customers = session.query(Customer).order_by(Customer.customerName).all()
    customers_list = [(c.customerNumber, c.customerName) for c in customers]
    add_order_form.customer.choices = customers_list

    if request.method == 'POST':

        if add_order_form.validate_on_submit():
            new_order = Order()

            new_order.customerNumber = add_order_form.customer.data
            new_order.orderDate = add_order_form.orderDate.data
            new_order.requiredDate = add_order_form.requiredDate.data
            new_order.shippedDate = add_order_form.shippedDate.data
            new_order.status = add_order_form.status.data
            new_order.comments = add_order_form.comments.data

            db.session.add(new_order)
            db.session.commit()

            return redirect("/orders")
        else:
            return render_template("orders/orders_add.html", customers=customers, form=add_order_form)
    else:
        return render_template("orders/orders_add.html", customers=customers, form=add_order_form)


@orders_blueprint.route("/orders/edit", methods=["GET", "POST"])
def orders_edit():
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    edit_order_form = OrderForm()

    customers = session.query(Customer).order_by(Customer.customerName).all()
    customers_list = [(c.customerNumber, c.customerName) for c in customers]
    edit_order_form.customer.choices = customers_list

    order_number = request.args["orderNumber"]

    # item laden (wie kann man einen datensatz lesen)
    order_to_edit = session.query(Order).filter(
        Order.orderNumber == order_number).first()

    if request.method == "POST":
        if edit_order_form.validate_on_submit():
            order_number = edit_order_form.orderNumber.data
            # update data here
            order_to_edit.orderDate = edit_order_form.orderDate.data
            order_to_edit.requiredDate = edit_order_form.requiredDate.data
            order_to_edit.shippedDate = edit_order_form.shippedDate.data
            order_to_edit.status = edit_order_form.status.data
            order_to_edit.comments = edit_order_form.comments.data
   
            order_to_edit.customerNumber = int(edit_order_form.customer.data)

            db.session.commit()
        return redirect("/orders")
    else:
        edit_order_form.orderNumber.data = order_to_edit.orderNumber

        # fill here
        edit_order_form.orderDate.data = order_to_edit.orderDate
        edit_order_form.requiredDate.data = order_to_edit.requiredDate
        edit_order_form.shippedDate.data = order_to_edit.shippedDate
        edit_order_form.status.data = order_to_edit.status
        edit_order_form.comments.data = order_to_edit.comments
        edit_order_form.customer.data = order_to_edit.customer

        return render_template("orders/orders_edit.html", customers=customers, form=edit_order_form)


@orders_blueprint.route("/orders/delete", methods=["post"])
def deleteorder():
    delete_item_form_obj = OrderDeleteForm()
    if delete_item_form_obj.validate_on_submit():

        order_code_to_delete = delete_item_form_obj.productCode.data
        product_to_delete = db.session.query(Product).filter(
            Product.productCode == product_code_to_delete)
        product_to_delete.delete()

        db.session.commit()
    else:
        print("Fatal Error")

    flash(f"Product with id {product_code_to_delete} has been deleted")

    return redirect("/products")
