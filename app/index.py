from flask import Blueprint, render_template

bp = Blueprint("golf", __name__, url_prefix="/")

@bp.route("/index", methods=["POST","GET"])
@bp.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")