from bs4 import BeautifulSoup as bs
import requests
import lxml
import json


url = "https://nbareplay.net/category/watch-nba-replay/"

count_games_file = open('number_game.txt', 'r')
count_games_on_web = int(count_games_file.read())
count_games_file.close()
matchs_dict = {}


def take_first_match(urls, last_game):

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    req = requests.get(urls, headers)

    with open("projects.html", "w") as file:
        file.write(req.text)

    with open("projects.html") as file:
        site = file.read()

    soup = bs(site, "lxml")
    try:
        first_match = soup.find('main', id='main').find(id=f'post-{last_game}').find_previous('article').get('id')
        first_match = first_match[-5:]

        return int(first_match)
    except Exception:
        return 0


def take_last_match(urls):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    req = requests.get(urls, headers)

    with open("projects.html", "w") as file:
        file.write(req.text)

    with open("projects.html") as file:
        site = file.read()

    soup = bs(site, "lxml")
    last_match_number = soup.find('main', id='main').find('article').get('id')
    last_match_number = last_match_number[-5:]

    return last_match_number


def get_video(urls, count_game):

    global links

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    req = requests.get(urls, headers)

    with open("projects.html", "w") as file:
        file.write(req.text)

    with open("projects.html") as file:
        site = file.read()

    soup = bs(site, "lxml")
    try:
        matchs = soup.find('main', id="main").find('article', id=f"post-{count_game}")
        match_title = matchs.find("div", class_="entry-title").find("h2").find('a').text
        match_link = matchs.find("div", class_="entry-title").find("h2").find('a').get('href')

        print(match_title)

        header = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
             Chrome/107.0.0.0 Safari/537.36'
        }

        req = requests.get(match_link, header)

        with open("projects_2.html", "w") as file:
            file.write(req.text)

        with open("projects_2.html") as file:
            site_2 = file.read()

        soup_2 = bs(site_2, "lxml")
        parts = soup_2.find('div', class_='entry-content').find(string='#FG by 4 Parts').find_parent('p').find_all('a')
        if (parts[0].get('href') is None) or (parts[1].get('href') is None) \
                or (parts[2].get('href') is None) or (parts[3].get('href') is None):
            print('Эта четверть еще не вышла...')
        else:
            part = [parts[0].get('href'), parts[1].get('href'), parts[2].get('href'), parts[3].get('href')]

            headers_1 = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/107.0.0.0 Safari/537.36"
            }

            links = []
            for i in part:

                req = requests.get(i, headers_1)

                with open("projects_3.html", "w") as file:
                    file.write(req.text)

                with open("projects_3.html") as file:
                    sites = file.read()

                soups = bs(sites, "lxml")
                if soups.find('div', class_='entry-content').find('iframe').get('src') is None:
                    print('Эта четверть еще не вышла...')
                else:
                    link = 'https:' + soups.find('div', class_='entry-content').find('iframe').get('src')
                    links.append(link)

            for link in links:
                print(link)



        matchs_dict[count_game] = {
            "match_title": match_title,
            "first_quarter": links[0],
            "second_quarter": links[1],
            "third_quarter": links[2],
            "fourth_quarter": links[3]
        }

        with open("../matchs_dict.json", "w") as file:
            json.dump(matchs_dict, file, indent=4, ensure_ascii=False)

    except Exception:
        print(f"Матча № {count_game} еще нету")
        return "Такого матча еще нету"


def main():
    if take_first_match(url, count_games_on_web) == 0:
        print('Данного матча еще нету')
    else:
        for match_number in range(take_first_match(url, count_games_on_web), int(take_last_match(url)) + 1):
            print('=' * 50)
            print('')
            get_video(url, match_number)
            print('')
            print('=' * 50)


if __name__ == "__main__":
    main()


f = open('number_game.txt', 'w')
f.write(take_last_match(url))
f.close()
