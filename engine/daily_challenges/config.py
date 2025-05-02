import os
import engine.daily_challenges.utils as utils
import engine.config as global_config


LAUNCH_TIME = utils.get_time_object(
    hour=6,
    minute=5
)

CATEGORIES = [
    'general',
    'bounty_hunter', 'naturalist', 'trader', 'collector', 'moonshiner'
]

DAILY_CHALLENGES_SOLUTIONS_DIR = os.path.join(global_config.SOLUTIONS_DIR, 'daily_challenges')
DAILY_CHALLENGES_ASSETS_DIR = os.path.join(global_config.ASSETS_DIR, 'daily_challenges')
DAILY_CHALLENGES_SOLUTIONS_IMAGES_DIR = os.path.join(DAILY_CHALLENGES_SOLUTIONS_DIR, 'images')
MADAM_NAZAR_LOCATION_MAPS_DIR = 'madam_nazar'
HEADER_COVER_BLANK = os.path.join(DAILY_CHALLENGES_ASSETS_DIR, 'daily_challenges_header_cover_blank.jpg')
HEADER_COVER = os.path.join(DAILY_CHALLENGES_ASSETS_DIR, 'daily_challenges_header_cover.jpg')
HEADER_GENERAL = os.path.join(DAILY_CHALLENGES_ASSETS_DIR, 'daily_challenges_header_general.jpg')
HEADER_ROLE = os.path.join(DAILY_CHALLENGES_ASSETS_DIR, 'daily_challenges_header_role.jpg')

CUSTOM_RDO_FONT = os.path.join(DAILY_CHALLENGES_ASSETS_DIR, 'chineserocksboldcyrillic.otf')

RDO_DAILY_CHALLENGES_API_URL = 'https://api.rdo.gg/challenges/index.json'
RDO_MADAM_NAZAR_LOCATION_URL = 'https://api.rdo.gg/nazar/'
