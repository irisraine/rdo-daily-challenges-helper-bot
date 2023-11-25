import requests
import json
import logging
from bs4 import BeautifulSoup
import engine.config as config

GENERAL_DAILY_CHALLENGES_COUNT = 7
ROLE_DAILY_CHALLENGES_COUNT = 3


def get_daily_challenges_api_response():
    response = get_response(config.RDO_DAILY_CHALLENGES_API_URL)
    if not response:
        return None
    daily_challenges_api_response = {}
    try:
        daily_challenges_raw = json.loads(response)
        for category in config.CATEGORIES:
            if category == 'general':
                daily_challenges_api_response.setdefault(category, [])
                for i in range(GENERAL_DAILY_CHALLENGES_COUNT):
                    current_challenge = daily_challenges_raw[category][i]
                    daily_challenges_api_response[category].append(normalize(current_challenge))
            else:
                daily_challenges_api_response.setdefault(category, [])
                for i in range(ROLE_DAILY_CHALLENGES_COUNT):
                    current_challenge = daily_challenges_raw['hard'][category][i]
                    daily_challenges_api_response[category].append(normalize(current_challenge))
    except (KeyError, TypeError):
        logging.error('Формат данных, полученных от RDO API, некорректен!')
        return None
    return daily_challenges_api_response


def get_madam_nazar_location_map_url():
    response = get_response(config.RDO_MADAM_NAZAR_LOCATION_URL)
    try:
        main_page_parsed = BeautifulSoup(response, 'html.parser')
        madam_nazar_location_map_url = main_page_parsed.find('main').find('img')['src']
    except (KeyError, TypeError):
        return None
    return madam_nazar_location_map_url


def normalize(current_challenge):
    daily_challenge_normalized = {
        'title': current_challenge['title'].lower(),
        'goal': current_challenge['goal']
    }
    return daily_challenge_normalized


def get_response(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Ответ от {url} успешно получен!")
            return response.content
        else:
            response.raise_for_status()
    except (requests.RequestException, requests.HTTPError):
        logging.error(f"Ошибка соединения с {url}")
        return None
    except requests.Timeout:
        logging.error(f"{url} не отвечает")
        return None
