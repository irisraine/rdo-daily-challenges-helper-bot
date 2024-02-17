# RDO Daily Challenges Helper bot

## Description

This Discord bot is designed to help players of the game Red Dead Online by posting tutorials for completing 
the daily challenges that are updated every 24 hours. The bot uses a free RDO API from the resource [api.rdo.gg](https://rdo.gg/api) 
to gather the latest information on the daily challenges.

## Commands

Bot publishes daily challenges guides automatically every 24h at 6:05 UTC.
- `$manual_publish` command - an emergency command that immediately publishes current daily guides. Use it only when automatic scheduled publishing did not work as expected, for example due to a hosting outage.

## Usage

Please make sure to specify the necessary environment variables. They should contain DISCORD_BOT_TOKEN and 
DAILY_CHALLENGES_TUTORIALS_CHANNEL environment variables and their corresponding values.
Here is an example:
```
# Bot token
DISCORD_BOT_TOKEN='your-discord-bot-token-here'
# Allowed channel
DAILY_CHALLENGES_TUTORIALS_CHANNEL=1111111111
```