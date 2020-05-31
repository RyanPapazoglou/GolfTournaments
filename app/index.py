from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("golf", __name__, url_prefix="/")

@bp.route("/index", methods=["POST","GET"])
@bp.route("/", methods=["POST","GET"])
@login_required
def index():
    return render_template("index.html")