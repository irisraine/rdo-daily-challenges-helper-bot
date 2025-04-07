import logging.config
import engine.config as config
from engine.bot import client


def run_discord_bot():
    logging.config.dictConfig(config.LOGGING_SETTINGS)
    client.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    run_discord_bot()
