import requests
from bs4 import BeautifulSoup
import re

from app.profile.profiles import Profiles
from app.scraper.scraper_dao import ScraperDao


class ScraperService:
    @staticmethod
    def update_standing(content):
        try:
            url = content["url"]
        except KeyError as e:
            return "URL not contained in content!"
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        tb = soup.find('table', class_='leaderboard')
        ScraperDao.reset_standings()
        for link in tb.find_all('tr', {"id": re.compile('player*')}):
            standing = link.find('td').getText()
            if 'T' in standing:
                standing = standing[1:]
            if int(standing) > 10:
                break
            name = link.find('td', class_='player').find('a').getText().split(' ', 1)
            first_name = name[0]
            last_name = name[1]
            ScraperDao.update_standings(first_name=first_name, last_name=last_name, standing=standing)
        Profiles.calculate_points()
        return True