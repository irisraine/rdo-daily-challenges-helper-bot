import nextcord
from nextcord.ext import commands, application_checks
import logging
import engine.config as config

client = commands.Bot(command_prefix='$', intents=nextcord.Intents.all(), default_guild_ids=[config.GUILD_ID])


@client.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                title="Ошибка", description="Публиковать гайды по дейликам могут только администраторы.",
                colour=nextcord.Color.red()), ephemeral=True
        )
    else:
        logging.error(f"При использовании команды произошла непредвиденная ошибка: {error}")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
