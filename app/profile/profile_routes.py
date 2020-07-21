import json

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.models import Users, UsersGolfers
from app.util import GolferEncoder
from app import db, START_TIME
import datetime

CURRENT_TIME = datetime.datetime.now()
bp = Blueprint("profile", __name__, url_prefix="/profile")

@bp.route('/<team_name>', methods=["POST","GET"])
@login_required
def profile(team_name):
    user = Users.query.filter_by(team_name=team_name).first_or_404()
    golfers_results = UsersGolfers.query.filter_by(user_id=user.id).all()
    golfers = ("["
        + ",".join(
            list(
                map(
                    lambda res: json.dumps(
                        res.golfer, cls=GolferEncoder
                    ),
                    golfers_results,
                )
            )
        )
        + "]"
    )
    golfers = json.loads(golfers)
    isRemovable = False if CURRENT_TIME > START_TIME else True
    return render_template('profile.html', user=user, golfers=golfers, count=(10-len(golfers)), isRemovable=isRemovable)

@bp.route('/remove', methods=["POST"])
@login_required
def remove():
    golfer_ids = request.form.getlist('check')
    for golfer_id in golfer_ids:
        users_golfers = UsersGolfers.query.filter_by(golfer_id=golfer_id).filter_by(user_id=current_user.id).first()
        db.session.delete(users_golfers)
    db.session.commit()
    return redirect(url_for('profile.profile', team_name=current_user.team_name))

@bp.route('/remove_all', methods=["POST"])
@login_required
def remove_all():
    users_golfers = UsersGolfers.query.filter_by(user_id=current_user.id).all()
    for golfer in users_golfers:
        db.session.delete(golfer)
    db.session.commit()
    return redirect(url_for('profile.profile', team_name=current_user.team_name))