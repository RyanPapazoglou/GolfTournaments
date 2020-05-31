from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Users

bp = Blueprint("profile", __name__, url_prefix="/profile")

@bp.route('/<team_name>', methods=["POST","GET"])
@login_required
def profile(team_name):
    user = Users.query.filter_by(team_name=team_name).first_or_404()
    golfers = user.golfers.all()
    return render_template('profile.html', user=user, golfers=golfers)