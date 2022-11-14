import re

from bs4 import BeautifulSoup as bs
import requests
import lxml
import json
from datetime import datetime

url = "https://nbareplay.net/category/watch-nba-replay/"

matchs_dict = {}

current_datetime = datetime.now()
current_day = current_datetime.day - 1
current_year = current_datetime.year
current_month = current_datetime.month

a = ['None', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

current_month_text = a[current_month % 12]


def get_links(urls):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers)

    with open("data/projects.html", "w") as file:
        file.write(req.text)

    with open("data/projects.html") as file:
        site = file.read()

    soup = bs(site, "lxml")

    try:
        matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(
            f'{current_day} {current_month_text} {current_year}'))

        for match in matchs_today:
            match_title = match.find('a').text
            match_link = match.find('a').get('href')



    except Exception:
        print("Такого матча нету")


get_links(url)
