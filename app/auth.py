from http import HTTPStatus
from flask import request, Blueprint, render_template

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST","GET"])
def login():
    content = request.json
    # if not content:
    #     return "Bad request. Expecting JSON.", HTTPStatus.BAD_REQUEST
    return render_template("base.html")
