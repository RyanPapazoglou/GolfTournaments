import pandas as pd
import os
import math
from app.golfers.golfers_dao import GolferDao


class GolfersGenerator:
    @staticmethod
    def read_golfer_data():
        golfers_df = pd.read_csv("app/golfers/3M Open Golfer File - PGA Golfers.csv")

        golfers_num_rows, golfers_num_cols = golfers_df.shape
        print("Rows: ", golfers_num_rows, "\nCols: ", golfers_num_cols)

        golfers_len = len(golfers_df.index)

        for i in range(0, golfers_len):
            odds = golfers_df.iloc[i, 3].split('/')
            try:
                res = int(odds[0])/int(odds[1])
                odds = int(res)*100
            except ValueError as e:
                print(e)
            picture_url = golfers_df.iloc[i, 5] if os.path.isfile('app/static/'+golfers_df.iloc[i, 5]) else 'default.png'
            world_rank = str(int(golfers_df.iloc[i, 2])) if not math.isnan(golfers_df.iloc[i, 2]) else 'N/A'
            GolferDao.store_golfer(first_name=str(golfers_df.iloc[i, 0]), last_name=str(golfers_df.iloc[i, 1]),
                                   world_rank=world_rank, odds=odds, odds_ratio=str(golfers_df.iloc[i, 3]),
                                   current_standing=int(golfers_df.iloc[i, 4]), current_points=None,
                                   picture_url=picture_url)
        print("Done.")

    @staticmethod
    def reset_standings():
        print("Resetting....")
        GolferDao.reset_standings()
        print("Done.")