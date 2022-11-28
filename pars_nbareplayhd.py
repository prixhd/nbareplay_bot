import re
import threading

from bs4 import BeautifulSoup as bs
import requests
import lxml
import json
from datetime import datetime
from tqdm import tqdm
from threading import *

matchs_dict = {}


def get_video(match):
    print('Матч обрабатывается!')
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    urls = "https://nbareplay.net/category/watch-nba-replay/"
    try:
        with requests.get(url=urls, headers=headers) as response:
            response_text = response.text

            soup = bs(response.text, "lxml")

            match_id = match.find_parent('article').get('id')[-5:]
            match_title = match.find('a').text
            match_link = match.find('a').get('href')

            header = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                         Chrome/107.0.0.0 Safari/537.36'
            }

            with requests.get(url=match_link, headers=header) as response:
                response_text = response.text

                soup_2 = bs(response_text, "lxml")

                parts = soup_2.find('div', class_='entry-content').find('strong', text=re.compile(
                    'FG by 4 Parts')).find_parent().find_all('a')

                part = []
                part_name = []
                for i in parts:
                    part_name.append(i.find('span').text[1:])
                    part.append(i.get('href'))

                links = []

                matchs_dict[match_id] = {
                    "match_title": match_title
                }

                headers_1 = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                     Chrome/107.0.0.0 Safari/537.36"
                }

                for i in part:
                    with requests.get(url=i, headers=headers_1) as response:
                        response_text = response.text

                        soups = bs(response_text, "lxml")
                        if soups.find('div', class_='entry-content').find('p').text == 'Uploading…':
                            continue
                        else:
                            link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
                            links.append(link)

                part_name_reversed = list(reversed(part_name))
                links_reversed = list(reversed(links))
                s = len(links)

                while s > 0:
                    data = ({f'{part_name_reversed[s - 1]}': links_reversed[s - 1]})
                    matchs_dict[match_id].update(data)
                    s -= 1
    except Exception:
        print('0')
    print('Матч обработан')


def get_matchs():
    global matchs_today
    current_datetime = datetime.now()
    current_day = current_datetime.day - 2
    current_year = current_datetime.year
    current_month = current_datetime.month

    a = ['None', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    current_month_text = a[current_month % 12]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    urls = "https://nbareplay.net/category/watch-nba-replay/"

    response = requests.get(url=urls, headers=headers)
    soup = bs(response.text, "lxml")
    try:
        matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(
            f'{current_day} {current_month_text} {current_year}'))
    except Exception:
        print('0')

    threads = []
    for i in range(len(matchs_today)-1):
        for matchs in matchs_today:
            thread = threading.Thread(
                target=get_video,
                args=[matchs]
            )
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    get_matchs()
    with open("matchs_dict.json", "w") as file:
        json.dump(matchs_dict, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()

# url = "https://nbareplay.net/category/watch-nba-replay/"
#
#
# def get_links(urls):
#     matchs_dict = {}
#
#     current_datetime = datetime.now()
#     current_day = current_datetime.day - 1
#     current_year = current_datetime.year
#     current_month = current_datetime.month
#
#     a = ['None', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#
#     current_month_text = a[current_month % 12]
#     headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
#              (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
#     }
#
#     req = requests.get(url, headers)
#
#     soup = bs(req.text, "lxml")
#
#     matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(
#         f'{current_day} {current_month_text} {current_year}'))
#
#     for match in tqdm(matchs_today):
#         match_id = match.find_parent('article').get('id')[-5:]
#         match_title = match.find('a').text
#         match_link = match.find('a').get('href')
#
#         header = {
#             "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
#              Chrome/107.0.0.0 Safari/537.36'
#         }
#
#         req = requests.get(match_link, header)
#
#         soup_2 = bs(req.text, "lxml")
#
#         parts = soup_2.find('div', class_='entry-content').find('strong', text=re.compile(
#             'FG by 4 Parts')).find_parent().find_all('a')
#         part = []
#         part_name = []
#         for i in parts:
#             part_name.append(i.find('span').text[1:])
#             part.append(i.get('href'))
#
#         headers_1 = {
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
#              Chrome/107.0.0.0 Safari/537.36"
#         }
#
#         links = []
#
#         matchs_dict[match_id] = {
#             "match_title": match_title
#         }
#
#         for i in part:
#             req = requests.get(i, headers_1)
#
#             soups = bs(req.text, "lxml")
#             if soups.find('div', class_='entry-content').find('p').text == 'Uploading…':
#                 continue
#             else:
#                 link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
#                 links.append(link)
#
#         part_name_reversed = list(reversed(part_name))
#         links_reversed = list(reversed(links))
#         s = len(links)
#         while s > 0:
#             data = ({f'{part_name_reversed[s - 1]}': links_reversed[s - 1]})
#             matchs_dict[match_id].update(data)
#             s -= 1
#
#         with open("matchs_dict.json", "w") as file:
#             json.dump(matchs_dict, file, indent=4, ensure_ascii=False)
#
#
# if __name__ == "__main__":
#     get_links(url)
