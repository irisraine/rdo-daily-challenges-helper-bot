# RDO Daily Challenges Helper bot

## Description

This Discord bot is designed to help players of the game Red Dead Online by posting tutorials for completing 
the daily challenges that are updated every 24 hours. The bot uses a free RDO API from the resource [api.rdo.gg](https://rdo.gg/api) to gather 
the latest information on the daily challenges.

## Usage

Please make sure to specify the necessary environment variables. They should contain DISCORD_BOT_TOKEN and 
DAILY_CHALLENGES_TUTORIALS_CHANNEL environment variables and their corresponding values.
Here is an example:
```
# Bot token
DISCORD_BOT_TOKEN='your-discord-bot-token-here'
# Allowed channels
ALLOWED_CHANNELS=1111111111, 2222222222
# API key of Microsoft Content Moderator service
CONTENT_MODERATOR_API_KEY='your-api-key-here'
```