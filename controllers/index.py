from flask import Flask
from flask.templating import render_template
from flask import Blueprint
from model.models import db,Customer

index_blueprint = Blueprint('index_blueprint', __name__)

@index_blueprint.route("/")
def index():
    customers = db.session.query(Customer).all()
    
    return render_template("index.html",customers=customers)