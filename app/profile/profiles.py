import json

from app.models import Users, UsersGolfers
from app.profile.profile_dao import ProfileDao
from app.util import GolferEncoder


class Profiles:
    @staticmethod
    def calculate_points():
        users = Users.query.all()
        for user in users:
            new_points = 0
            golfers = UsersGolfers.query.filter_by(user_id=user.id).all()
            golfers = ("["
                       + ",".join(
                        list(
                            map(
                                lambda res: json.dumps(
                                    res.golfer, cls=GolferEncoder
                                ),
                                golfers,
                            )
                        )
                    )
                + "]"
            )
            golfers = json.loads(golfers)
            for golfer in golfers:
                if golfer['current_standing'] and golfer['current_standing'] < 11:
                    new_points += golfer['current_points']
            ProfileDao.set_points(user, new_points)

    @staticmethod
    def reset_points():
        print("Resetting....")
        ProfileDao.reset_points()
        print("Done.")