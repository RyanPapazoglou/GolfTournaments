import os
import requests

class ScraperJob:
    @staticmethod
    def scrape():
        try:
            print('Updating Standings!')
            url = 'http://www.espn.com/golf//leaderboard'
            requests.post(
                f"{os.getenv('SCRAPE_HOME')}/standings/update",
                json={
                    "url": url
                },
            )
        except Exception as e:
            print("Error with getting events", e)
            return False
        return True

