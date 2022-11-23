import re, json, lxml, requests, asyncio, aiohttp
from bs4 import BeautifulSoup as bs
from datetime import datetime
from tqdm import tqdm

matchs_dict = {}
print(datetime.now())


async def get_video(session, match):
    print('Идет обработка...')
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    url = "https://nbareplay.net/category/watch-nba-replay/"

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = bs(await response.text(), "lxml")
        try:
            match_id = match.find_parent('article').get('id')[-5:]
            match_title = match.find('a').text
            match_link = match.find('a').get('href')

            header = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                     Chrome/107.0.0.0 Safari/537.36'
            }

            async with session.get(url=match_link, headers=header) as response:
                response_text = await response.text()

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
                    async with session.get(url=i, headers=headers_1) as response:
                        response_text = await response.text()

                        soups = bs(response_text, "lxml")
                        if soups.find('div', class_='entry-content').find('p').text == 'Uploading...':
                            continue
                        else:
                            link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
                            links.append(link)

                part_name_reversed = list(reversed(part_name))
                links_reversed = list(reversed(links))
                s = len(links)

                while s > 0:
                    data = ({f'{part_name_reversed[s-1]}': links_reversed[s-1]})
                    matchs_dict[match_id].update(data)
                    s -= 1
        except Exception:
            print('0')

    print(f'Матч обработан!')


async def get_matchs():
    current_datetime = datetime.now()
    current_day = current_datetime.day - 1
    current_year = current_datetime.year
    current_month = current_datetime.month

    a = ['None', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    current_month_text = a[current_month % 12]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    url = "https://nbareplay.net/category/watch-nba-replay/"

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = bs(await response.text(), "lxml")
        try:
            matchs_today = soup.find('main', id="main").find_all('h2', text=re.compile(
                f'{current_day} {current_month_text} {current_year}'))
        except Exception:
            print('0')
        tasks = []

        for matchs in matchs_today:
            task = asyncio.create_task(get_video(session, matchs))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(get_matchs())
    with open("matchs_dict.json", "w") as file:
        json.dump(matchs_dict, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
    print(datetime.now())
