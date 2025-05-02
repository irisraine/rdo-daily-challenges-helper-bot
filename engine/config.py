import os
from dotenv import load_dotenv


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
TROUBLESHOOTING_GUIDES_CHANNEL_ID = int(os.getenv('TROUBLESHOOTING_GUIDES_CHANNEL'))

BASIC_COLOR_CODE = (48, 213, 200)

ASSETS_DIR = 'assets'
SOLUTIONS_DIR = 'solutions'

SEPARATOR = os.path.join(ASSETS_DIR, 'separator.png')
