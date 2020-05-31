from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from app import db
from app.models import Golfers, UsersGolfers

bp = Blueprint("golfers", __name__, url_prefix="/golfers")

@bp.route("/select", methods=["GET"])
def select():
    golfers = Golfers.query.all()
    current_golfers = len(UsersGolfers.query.filter_by(user_id=current_user.id).all())
    return render_template("golfers.html", golfers=golfers, count=current_golfers)

@bp.route("/submit", methods=["POST"])
def submit():
    golfer_ids = request.form.getlist('check')
    if len(golfer_ids) > 10:
        flash("You can only select a max of 10 golfers! Try again.")
        return redirect(url_for("golfers.select"))
    try:
        current_golfers = UsersGolfers.query.filter_by(user_id=current_user.id).all()
        if len(current_golfers) >= 10:
            flash("Your team is already full!")
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