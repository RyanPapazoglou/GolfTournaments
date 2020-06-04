import pandas as pd
from app.golfers.golfers_dao import GolferDao


class GolfersGenerator:
    @staticmethod
    def read_golfer_data():
        golfers_df = pd.read_csv("app/golfers/PGA Championship Golfer File - PGA Golfers.csv")

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
            GolferDao.store_golfer(first_name=str(golfers_df.iloc[i, 0]), last_name=str(golfers_df.iloc[i, 1]),
                             world_rank=str(golfers_df.iloc[i, 2]), odds=odds, odds_ratio=str(golfers_df.iloc[i, 3]), current_standing=int(golfers_df.iloc[i, 4]),
                             picture_url=str(golfers_df.iloc[i, 5]))
        print("Done.")

    @staticmethod
    def reset_standings():
        print("Resetting....")
        GolferDao.reset_standings()
        print("Done.")