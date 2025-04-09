import json
import logging
import engine.config as config
from engine.utils import get_response_content


def get_daily_challenges_api_response():
    response = get_response_content(config.RDO_DAILY_CHALLENGES_API_URL)
    if not response:
        return
    daily_challenges_api_response = {}
    try:
        daily_challenges_raw = json.loads(response)
        for category in config.CATEGORIES:
            if category == 'general':
                daily_challenges_api_response.setdefault(category, [])
                for i in range(7):
                    current_challenge = daily_challenges_raw[category][i]
                    daily_challenges_api_response[category].append(_normalize(current_challenge))
            else:
                daily_challenges_api_response.setdefault(category, [])
                for i in range(3):
                    current_challenge = daily_challenges_raw['hard'][category][i]
                    daily_challenges_api_response[category].append(_normalize(current_challenge))
    except (KeyError, TypeError):
        logging.error('Формат данных, полученных от RDO API, некорректен!')
        return
    return daily_challenges_api_response


def get_madam_nazar_location_api_response():
    response = get_response_content(config.RDO_MADAM_NAZAR_LOCATION_URL)
    if not response:
        return
    madam_nazar_location_raw = json.loads(response)
    madam_nazar_location_api_response = madam_nazar_location_raw['location']
    return madam_nazar_location_api_response


def _normalize(current_challenge):
    daily_challenge_normalized = {
        'title': current_challenge['title'].lower(),
        'goal': current_challenge['goal']
    }
    return daily_challenge_normalized
