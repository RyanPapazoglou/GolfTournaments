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
            GolferDao.store_golfer(first_name=str(golfers_df.iloc[i, 0]), last_name=str(golfers_df.iloc[i, 1]),
                             world_rank=str(golfers_df.iloc[i, 2]), odds=str(golfers_df.iloc[i, 3]),
                             picture_url=str(golfers_df.iloc[i, 4]))
        print("Done.")