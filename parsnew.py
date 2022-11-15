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
        matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(f'{current_day} {current_month_text} {current_year}'))

        for match in matchs_today:
            match_id = match.find_parent('article').get('id')[-5:]
            match_title = match.find('a').text
            match_link = match.find('a').get('href')

            header = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/107.0.0.0 Safari/537.36'
            }

            req = requests.get(match_link, header)

            with open("data/projects_2.html", "w") as file:
                file.write(req.text)

            with open("data/projects_2.html") as file:
                site_2 = file.read()

            soup_2 = bs(site_2, "lxml")

            parts = soup_2.find('div', class_='entry-content').find('strong', text=re.compile('FG by 4 Parts')).find_parent().find_all('a')
            part = [parts[0].get('href'), parts[1].get('href'), parts[2].get('href'), parts[3].get('href')]

            headers_1 = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/107.0.0.0 Safari/537.36"
            }
            links = []
            for i in part:
                req = requests.get(i, headers_1)

                with open("data/projects_3.html", "w") as file:
                    file.write(req.text)

                with open("data/projects_3.html") as file:
                    sites = file.read()

                soups = bs(sites, "lxml")

                link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
                links.append(link)

            matchs_dict[match_id] = {
                "match_title": match_title,
                "first_quarter": links[0],
                "second_quarter": links[1],
                "third_quarter": links[2],
                "fourth_quarter": links[3]
            }

            with open("matchs_dict.json", "w") as file:
                json.dump(matchs_dict, file, indent=4, ensure_ascii=False)
    except Exception:
        print('0')


get_links(url)
