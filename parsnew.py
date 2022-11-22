import re
from bs4 import BeautifulSoup as bs
import requests
import lxml
import json
from datetime import datetime

url = "https://nbareplay.net/category/watch-nba-replay/"

print(datetime.now())

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

    soup = bs(req.text, "lxml")
    try:
        matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(
            f'{current_day} {current_month_text} {current_year}'))

        for match in matchs_today:
            match_id = match.find_parent('article').get('id')[-5:]
            match_title = match.find('a').text
            match_link = match.find('a').get('href')

            header = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/107.0.0.0 Safari/537.36'
            }

            req = requests.get(match_link, header)

            soup_2 = bs(req.text, "lxml")

            parts = soup_2.find('div', class_='entry-content').find('strong', text=re.compile(
                'FG by 4 Parts')).find_parent().find_all('a')
            part = []
            part_name = []
            for i in parts:
                if i.get('href') is None:
                    continue
                else:
                    part_name.append(i.find('span').text[1:])
                    part.append(i.get('href'))

            headers_1 = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/107.0.0.0 Safari/537.36"
            }

            links = []

            matchs_dict[match_id] = {
                "match_title": match_title
            }

            for i in part:
                req = requests.get(i, headers_1)

                soups = bs(req.text, "lxml")

                link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
                links.append(link)

            part_name_reversed = list(reversed(part_name))
            links_reversed = list(reversed(links))
            s = len(links)
            while s > 0:
                data = ({f'{part_name_reversed[s-1]}': links_reversed[s-1]})
                matchs_dict[match_id].update(data)
                s -= 1

            with open("matchs_dict.json", "w") as file:
                json.dump(matchs_dict, file, indent=4, ensure_ascii=False)
    except Exception:
        print('0')


if __name__ == "__main__":
    get_links(url)
    print(datetime.now())
