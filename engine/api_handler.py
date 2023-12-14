import json
import logging
import engine.config as config
from engine.network import get_response_content

GENERAL_DAILY_CHALLENGES_COUNT = 7
ROLE_DAILY_CHALLENGES_COUNT = 3


def get_daily_challenges_api_response():
    response = get_response_content(config.RDO_DAILY_CHALLENGES_API_URL)
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


def get_madam_nazar_location_api_response():
    response = get_response_content(config.RDO_MADAM_NAZAR_LOCATION_URL)
    if not response:
        return None
    madam_nazar_location_raw = json.loads(response)
    madam_nazar_location = madam_nazar_location_raw['location']
    return madam_nazar_location


def normalize(current_challenge):
    daily_challenge_normalized = {
        'title': current_challenge['title'].lower(),
        'goal': current_challenge['goal']
    }
    return daily_challenge_normalized
