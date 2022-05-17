from flask import Flask, redirect, request, flash
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
import sqlalchemy.orm

from forms.OrderForm import OrderForm
from forms.OrderdetailDeleteForm import OrderdetailDeleteForm
from forms.OrderdetailForm import OrderdetailForm
from model.models import Customer, Order, Orderdetail, Product, db, Orderdetail


orderdetails_blueprint = Blueprint('orderdetails_blueprint', __name__)


@orderdetails_blueprint.route("/orderdetails/edit", methods=["GET", "POST"])
def orders_edit():
    session: sqlalchemy.orm.scoping.scoped_session = db.session

    order_detail_form = OrderdetailForm()
    products = session.query(Product).order_by(Product.productCode).all()
    product_list = [(str(p.productCode), p.productName)
                    for p in products]
    order_detail_form.productCode.choices = product_list

    order_number = int(request.args["orderNumber"])
    product_code = request.args["productCode"]
    order_detail_form.productCode.choices
    order_detail_query: sqlalchemy.orm.query.Query = session.query(Orderdetail)
    order_detail_to_edit: Orderdetail = order_detail_query.filter(
        sqlalchemy.and_(
            Orderdetail.orderNumber == order_number,
            Orderdetail.productCode == product_code)).first()

    if request.method == "POST":
        if order_detail_form.validate_on_submit():

            order_detail_to_edit.priceEach = order_detail_form.priceEach.data
            order_detail_to_edit.quantityOrdered = order_detail_form.quantityOrdered.data

            db.session.commit()
        return redirect("/orders")
    else:
        order_detail_form.orderNumber.data = order_detail_to_edit.orderNumber
        order_detail_form.productCode.data = order_detail_to_edit.productCode
        order_detail_form.orderLineNumber.data = order_detail_to_edit.orderLineNumber
        order_detail_form.priceEach.data = order_detail_to_edit.priceEach
        order_detail_form.quantityOrdered.data = order_detail_to_edit.quantityOrdered

        return render_template("order_details/order_detail_edit.html", form=order_detail_form)


@orderdetails_blueprint.route("/orderdetails/delete", methods=["post"])
def deleteorder():
    delete_item_form_obj = OrderdetailDeleteForm()
    if delete_item_form_obj.validate_on_submit():

        order_number_to_delete = int(delete_item_form_obj.orderNumber.data)
        product_code_to_delete = (delete_item_form_obj.productCode.data)
        orderdetail_to_delete = db.session.query(Orderdetail).filter(
            sqlalchemy.and_(
                Orderdetail.orderNumber == order_number_to_delete,
                Orderdetail.productCode == product_code_to_delete)
        )
        orderdetail_to_delete.delete()

        db.session.commit()
    else:
        print("Fatal Error")

    flash(f"Product with id {product_code_to_delete} has been deleted")

    return redirect("/orders/edit?orderNumber=" + str(order_number_to_delete))
