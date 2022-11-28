import re
from bs4 import BeautifulSoup as bs
import requests
import lxml
import json
from datetime import datetime
import datetime
from auth_data import token

matchs_dict = {}


def get_video_date(date):
    target_date_time_ms = int(str(date) + '000')
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, int(target_date_time_ms))
    target_date = base_datetime + delta
    current_day = target_date.day
    current_year = target_date.year
    current_month = target_date.month
    return f'{current_year}-{current_month}-{current_day}'


def get_now_date():
    current_datetime = datetime.datetime.now()
    current_day = current_datetime.day - 1
    current_year = current_datetime.year
    current_month = current_datetime.month
    return f'{current_year}-{current_month}-{current_day}'


def get_video_posts():
    url = f"https://api.vk.com/method/video.get?domain=all_about_nba&owner_id=-55574239&access_token={token}&v=5.131"
    req = requests.get(url)
    src = req.json()

    video = src['response']["items"]
    matchs_data = []
    for match_data in video:
        match_data = match_data['adding_date']
        matchs_data.append(match_data)

    for i in range(0, 100):
        match_id = video[i]['adding_date']
        date = get_video_date(match_id)
        video_title = video[i]['title']
        match_title = f'{video_title}'
        match_link = video[i]['player']
        if 'НБА 22/23' in video_title:
            if get_now_date() == date:
                matchs_dict[match_id] = {
                    'match_title': match_title,
                    'full_game': match_link
                }

                with open("data/matchs_dict_aanba_vk.json", "w", encoding="utf-8") as file:
                    json.dump(matchs_dict, file, indent=4, ensure_ascii=False)


def main():
    get_video_posts()


if __name__ == '__main__':
    main()
