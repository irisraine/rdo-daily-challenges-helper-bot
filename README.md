# RDO Helper bot

## Description

This Discord bot is designed to help players of the game Red Dead Online by providing two major functionalities:

1. **Daily Challenges Guides**

Automatically posts tutorials for completing daily challenges updated every 24 hours. 
It uses the free RDO API from [api.rdo.gg](https://rdo.gg/api) to gather the latest information on the daily challenges. 
The bot publishes the daily challenges guides at 6:05 UTC.

2. **Troubleshooting Guides**

Offers a collection of authored guides containing solutions to a variety of issues and bugs in Red Dead Online, as well as helpful explanations of game features.

## Commands

* `/daily_challenges` - Immediately publishes the current daily challenge guides. Use this as a fallback when scheduled posting fails (e.g., due to a hosting issue).
* `/troubleshooting` - Posts the troubleshooting guides interface into the specified channel, allowing users to explore available help topics interactively.
* `/update <filename.json>` - Allows uploading and updating of the troubleshooting guides via a JSON file containing the updated guide data.
* `/current <group>` - Get JSON file with current troubleshooting guides of selected group.

## Usage

Please make sure to specify the necessary environment variables. They should contain DISCORD_BOT_TOKEN, 
DAILY_CHALLENGES_TUTORIALS_CHANNEL and TROUBLESHOOTING_GUIDES_CHANNEL environment variables and their corresponding values.
Here is an example:
```
# Bot token
DISCORD_BOT_TOKEN='your-discord-bot-token-here'
# ID of your server
GUILD_ID = 0000000000000000000
# Allowed channel
DAILY_CHALLENGES_TUTORIALS_CHANNEL=0000000000000000000
TROUBLESHOOTING_GUIDES_CHANNEL=0000000000000000000
```