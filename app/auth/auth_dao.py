from werkzeug.security import generate_password_hash

from app import db
from app.models import Users


class AuthDao:
    @staticmethod
    def update_password(team_name, new_password):
        user = Users.query.filter_by(team_name=team_name).first()
        try:
            user.password = generate_password_hash(new_password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
        print("Done.")