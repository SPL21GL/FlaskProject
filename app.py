from flask import Flask
from model.models import db
from flask.templating import render_template
from controllers.index import index_blueprint
from controllers.products import products_blueprint
from flask_wtf.csrf import CSRFProtect

import sqlalchemy
app = Flask(__name__)
app.secret_key = "VerySecretSecretKey"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/classicmodels"

csrf = CSRFProtect(app)

db.init_app(app)

#hier blueprint registrieren
app.register_blueprint(index_blueprint)
app.register_blueprint(products_blueprint)

app.run(debug=True)