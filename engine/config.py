import os
from dotenv import load_dotenv
import engine.utils as utils


load_dotenv()

LOGGING_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s][%(asctime)s] : %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }
}

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
DAILY_CHALLENGES_TUTORIALS_CHANNEL_ID = int(os.getenv('DAILY_CHALLENGES_TUTORIALS_CHANNEL'))

LAUNCH_TIME = utils.get_time_object(
    hour=6,
    minute=5
)

CATEGORIES = [
    'general',
    'bounty_hunter', 'naturalist', 'trader', 'collector', 'moonshiner'
]

BASIC_COLOR_CODE = (48, 213, 200)

ASSETS_DIR = 'assets'
SOLUTIONS_DIR = 'solutions'
SOLUTIONS_IMAGES_DIR = os.path.join(SOLUTIONS_DIR, 'images')
MADAM_NAZAR_LOCATION_MAPS_DIR = 'madam_nazar'
HEADER_COVER_BLANK = os.path.join(ASSETS_DIR, 'daily_challenges_header_cover_blank.jpg')
HEADER_COVER = os.path.join(ASSETS_DIR, 'daily_challenges_header_cover.jpg')
HEADER_GENERAL = os.path.join(ASSETS_DIR, 'daily_challenges_header_general.jpg')
HEADER_ROLE = os.path.join(ASSETS_DIR, 'daily_challenges_header_role.jpg')
SEPARATOR = os.path.join(ASSETS_DIR, 'separator.png')

CUSTOM_RDO_FONT = os.path.join(ASSETS_DIR, 'chineserocksboldcyrillic.otf')

RDO_DAILY_CHALLENGES_API_URL = 'https://api.rdo.gg/challenges/index.json'
RDO_MADAM_NAZAR_LOCATION_URL = 'https://api.rdo.gg/nazar/'
