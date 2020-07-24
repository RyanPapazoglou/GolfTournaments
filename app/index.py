from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import desc
from app.models import Users, Golfers
from app import local

bp = Blueprint("golf", __name__, url_prefix="/")

@bp.route("/index", methods=["POST","GET"])
@bp.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

@bp.route("/leaderboard", methods=["POST","GET"])
@login_required
def leaderboard():
    golfer_update = Golfers.query.filter(Golfers.updated_at != None).first()
    update = golfer_update.updated_at.astimezone(local).strftime("%B %d, %Y %I:%M:%S %p EST")
    players=Users.query.order_by(desc(Users.points)).all()
    return render_template("leaderboard.html", players=players, update=update)