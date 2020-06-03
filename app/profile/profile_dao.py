from app import db
from app.models import Users


class ProfileDao:
    @staticmethod
    def set_points(user, points):
        try:
            user.points = points
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "User's points updated"

    @staticmethod
    def reset_points():
        try:
            Users.query.update({Users.points: 0})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "Points reset"