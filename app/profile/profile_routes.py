import json

from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Users, UsersGolfers
from app.util import GolferEncoder

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
    return render_template('profile.html', user=user, golfers=golfers, count=(10-len(golfers)))