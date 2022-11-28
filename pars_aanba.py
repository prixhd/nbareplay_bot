import re
from bs4 import BeautifulSoup as bs
import requests
import lxml
import json
from datetime import datetime

from lxml.doctestcompare import strip
from tqdm import tqdm

matchs_dict = {}

current_datetime = datetime.now()
current_day = current_datetime.day
current_year = current_datetime.year
current_month = current_datetime.month

a = ['None', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
     'декабря']

current_month_text = a[current_month % 12]
url = "https://aanba.ru/zapisi-matchej"


def get_video_rus(urls):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    req = requests.get(url, headers)
    soup = bs(req.text, "lxml")

    matchs_today = soup.find('div', class_='p-mf').find_all('span', text=re.compile(f'{current_day} {current_month_text} {current_year}'))

    links = []
    for match in matchs_today:
        match_link = "https://aanba.ru/" + match.find_parent('a').get('href')
        req_1 = requests.get(match_link, headers)
        soup_1 = bs(req_1.text, "lxml")
        match_video = soup_1.find('div', class_="snippet").find('iframe').get('src')
        if match_video[8:14] != "vk.com":
            continue
        else:
            match_id = match.find_parent(class_='mf-3').find_parent().get('class')[-1][-5:]
            links.append(match_video)
            match_title_1 = soup_1.find('div', id='yoo-zoo')\
                .find('div', class_='row')\
                .find('div', class_='mf-1').text

            match_title_2 = soup_1.find('div', id='yoo-zoo')\
                .find('div', class_='row')\
                .find('div', class_='mf-5').text

            match_title = f'{strip(match_title_1)} / {strip(match_title_2)}'

            matchs_dict[match_id] = {
                'match_title': match_title,
                'full_game': match_video
            }

            with open("data/matchs_dict_aanba.json", "w") as file:
                json.dump(matchs_dict, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_video_rus(url)