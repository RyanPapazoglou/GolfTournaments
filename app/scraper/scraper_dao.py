import datetime
from sqlalchemy import func
from app import db
from app.models import Golfers


class ScraperDao:
    @staticmethod
    def reset_standings():
        try:
            Golfers.query.update({Golfers.current_standing: 0})
            Golfers.query.update({Golfers.current_points: 0})
            Golfers.query.update({Golfers.updated_at: None})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return True

    @staticmethod
    def update_standings(first_name, last_name, standing):
        try:
            golfer = (
                db.session.query(Golfers)
                .filter(
                    func.lower(Golfers.first_name) == func.lower(first_name),
                    func.lower(Golfers.last_name) == func.lower(last_name),
                )
                .first()
            )
            if golfer:
                golfer.current_standing = standing
                golfer.current_points = (
                    golfer.odds * (1.1 - (0.1 * int(standing)))
                    if int(standing) <= 10
                    else 0
                )
                golfer.updated_at = datetime.datetime.now()
                db.session.add(golfer)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return "Error" + str(e)
        return "Standings set"
