import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db, START_TIME, local
from app.models import Golfers, UsersGolfers

bp = Blueprint("golfers", __name__, url_prefix="/golfers")

@bp.route("/select", methods=["GET"])
@login_required
def select():
    if datetime.datetime.now() > START_TIME:
        return render_template("closed.html")
    golfers = Golfers.query.order_by(Golfers.odds, Golfers.world_rank).all()
    current_golfers = UsersGolfers.query.filter_by(user_id=current_user.id).all()
    golfer_ids = []
    for golfer in current_golfers:
        golfer_ids.append(golfer.golfer_id)
    golfers = [golfer for golfer in golfers if golfer.id not in golfer_ids]
    EST_TIME = START_TIME.astimezone(local).strftime("%B %d, %Y %I:%M:%S %p EST")
    return render_template("golfers.html", golfers=golfers, count=len(current_golfers), start_time=EST_TIME)

@bp.route("/submit", methods=["POST"])
@login_required
def submit():
    if datetime.datetime.now() > START_TIME:
        return render_template("closed.html")
    golfer_ids = request.form.getlist('check')
    if len(golfer_ids) > 10:
        flash("You can only select a max of 10 golfers! Try again.")
        return redirect(url_for("golfers.select"))
    try:
        current_golfers = UsersGolfers.query.filter_by(user_id=current_user.id).all()
        if (len(current_golfers) + len(golfer_ids)) > 10:
            flash("This selection has put your team above 10 golfers, please check your current team and try again.")
            return redirect(url_for('profile.profile', team_name=current_user.team_name))
        for golfer_id in golfer_ids:
            users_golfers = UsersGolfers(user_id=current_user.id, golfer_id=golfer_id)
            db.session.add(users_golfers)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("An error occurred. It is likely one or more golfers selected is already on your team. Please check your team page.")
    return redirect(url_for('profile.profile', team_name=current_user.team_name))