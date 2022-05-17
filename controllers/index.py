from flask.templating import render_template
from flask import Blueprint

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route("/")
def index():

    return render_template("index.html")
