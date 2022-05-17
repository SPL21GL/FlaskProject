from flask import Flask, redirect, request, flash
from flask.templating import render_template
from flask import Blueprint
import sqlalchemy
import sqlalchemy.orm

from forms.OrderForm import OrderForm
from forms.OrderdetailDeleteForm import OrderdetailDeleteForm
from model.models import Customer, Order, Orderdetail, db, Orderdetail


orderdetails_blueprint = Blueprint('orderdetails_blueprint', __name__)




@orderdetails_blueprint.route("/orderdetails/edit", methods=["GET", "POST"])
def orders_edit():
    session: sqlalchemy.orm.scoping.scoped_session = db.session
    
    edit_order_form = OrderForm()
    
    customers = session.query(Customer).order_by(Customer.customerName).all()
    customers_list = [(str(c.customerNumber), c.customerName) for c in customers]
    edit_order_form.customer.choices = customers_list
    
    order_number = request.args["orderNumber"]

    order_detail_query : sqlalchemy.orm.query.Query = session.query(Orderdetail)
    order_details = order_detail_query.filter(Orderdetail.orderNumber == order_number).order_by(Orderdetail.orderLineNumber).all()

    # item laden (wie kann man einen datensatz lesen)
    order_to_edit = session.query(Order).filter(
        Order.orderNumber == order_number).first()

    if request.method == "POST":
        if edit_order_form.validate_on_submit():
            #order_number = edit_order_form.orderNumber.data
            # update data here
            order_to_edit.orderDate = edit_order_form.orderDate.data
            order_to_edit.requiredDate = edit_order_form.requiredDate.data
            order_to_edit.shippedDate = edit_order_form.shippedDate.data
            order_to_edit.status = edit_order_form.status.data
            order_to_edit.comments = edit_order_form.comments.data
            
            print(f"CustomerBefore: {order_to_edit.customerNumber}")
            print(f"Customer: {edit_order_form.customer.data}")
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
        edit_order_form.customer.data = str(order_to_edit.customerNumber)
        return render_template("orders/orders_edit.html", customers=customers, form=edit_order_form, order_details = order_details)





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
