from sqlalchemy import and_, func

from app import db
from app.models import Golfers

class GolferDao:
    @staticmethod
    def store_golfer(first_name, last_name, world_rank, odds, odds_ratio, current_standing, picture_url, current_points):
        try:
            golfer = Golfers(first_name=first_name, last_name=last_name,
                             world_rank=world_rank, odds=odds, odd_ratio=odds_ratio,
                             current_standing=current_standing, picture_url=picture_url,
                             updated_at=None, current_points=current_points)
            db.session.add(golfer)
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "Golfer Added"

    @staticmethod
    def reset_standings():
        try:
            Golfers.query.update({Golfers.current_standing: 0})
            Golfers.query.update({Golfers.current_points: 0})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "Standings reset"

    @staticmethod
    def update_standing(first_name, last_name, standing):
        try:
            golfer = db.session.query(Golfers).filter(
                func.lower(Golfers.first_name)==func.lower(first_name),
                func.lower(Golfers.last_name)==func.lower(last_name)).first()
            if golfer:
                golfer.current_standing = standing
                golfer.current_points = golfer.odds * (1.1-(.1 * standing))
                db.session.add(golfer)
                db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "Standings set"