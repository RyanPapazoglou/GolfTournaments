import os
import requests


class ScraperJob:
    @staticmethod
    def scrape():
        try:
            print("Starting job to update standings")
            url = "http://www.espn.com/golf//leaderboard"
            requests.post(
                f"{os.getenv('SCRAPE_HOME')}/standings/update", json={"url": url},
            )
            print("Finished job")
        except Exception as e:
            print("Error with getting events", e)
            return False
        return True
