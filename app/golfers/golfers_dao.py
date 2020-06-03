from app import db
from app.models import Golfers

class GolferDao:
    @staticmethod
    def store_golfer(first_name, last_name, world_rank, odds, odds_ratio, current_standing, picture_url):
        try:
            golfer = Golfers(first_name=first_name, last_name=last_name,
                             world_rank=world_rank, odds=odds, odd_ratio=odds_ratio, current_standing=current_standing, picture_url=picture_url)
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
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error" + str(e)
        return "Standings reset"