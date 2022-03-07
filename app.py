from flask import Flask
from model.models import db
from flask.templating import render_template
from controllers.index import index_blueprint

app = Flask(__name__)
app.secret_key = "VerySecretSecretKey"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/classicmodels"
db.init_app(app)

app.register_blueprint(index_blueprint)

app.run(debug=True)