import requests
import json
import engine.config as config
from bs4 import BeautifulSoup

RDO_DAILY_CHALLENGES_API_URL = 'https://api.rdo.gg/challenges/index.json'
RDO_MADAM_NAZAR_LOCATION_URL = 'https://rdocollector.com/madam-nazar'
GENERAL_DAILY_CHALLENGES_COUNT = 7
ROLE_DAILY_CHALLENGES_COUNT = 3


def get_daily_challenges():
    response = get_response(RDO_DAILY_CHALLENGES_API_URL)

    daily_challenges = {}
    try:
        daily_challenges_raw = json.loads(response)
        for category in config.CATEGORIES:
            if category == 'general':
                daily_challenges.setdefault(category, [])
                for i in range(GENERAL_DAILY_CHALLENGES_COUNT):
                    current_challenge = daily_challenges_raw[category][i]
                    daily_challenges[category].append(normalize(current_challenge))
            else:
                daily_challenges.setdefault(category, [])
                for i in range(ROLE_DAILY_CHALLENGES_COUNT):
                    current_challenge = daily_challenges_raw['hard'][category][i]
                    daily_challenges[category].append(normalize(current_challenge))
    except (KeyError, TypeError):
        print('Формат данных, полученных от RDO API, некорректен')
        return None
    return daily_challenges


def get_madam_nazar_location():
    response = get_response(RDO_MADAM_NAZAR_LOCATION_URL)
    try:
        main_page_parsed = BeautifulSoup(response, 'html.parser')
        madam_nazar_location = main_page_parsed.find('main').find('img')['src']
    except (KeyError, TypeError):
        return None
    return madam_nazar_location


def normalize(current_challenge):
    daily_challenge_normalized = {
            'title': current_challenge['title'].lower(),
            'goal': current_challenge['goal']
        }
    return daily_challenge_normalized


def get_response(url):
    try:
        response = requests.get(url)
        return response.content
    except requests.RequestException:
        print(f"Ошибка соединения с {url}")
        return None
