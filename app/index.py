from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import desc
from app.models import Users

bp = Blueprint("golf", __name__, url_prefix="/")

@bp.route("/index", methods=["POST","GET"])
@bp.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

@bp.route("/leaderboard", methods=["POST","GET"])
@login_required
def leaderboard():
    players=Users.query.order_by(desc(Users.points)).all()
    return render_template("leaderboard.html", players=players)