import nextcord
from nextcord.ext import commands, tasks, application_checks
import logging
import engine.config as config
import engine.messages as messages

client = commands.Bot(command_prefix='$', intents=nextcord.Intents.all(), default_guild_ids=[config.GUILD_ID])


async def daily_challenges_guide():
    message_channel = client.get_channel(config.TARGET_CHANNEL_ID)

    header_messages = messages.get_header_messages()
    tutorial_messages = messages.get_tutorial_messages()
    madam_nazar_location_message = messages.get_madam_nazar_location_message()

    if not tutorial_messages:
        logging.error("Данные о дейликах не могут быть отображены из-за ошибки")
        return

    await message_channel.send(
        embed=header_messages['cover'].embed,
        file=header_messages['cover'].image
    )
    for category in ('general', 'role'):
        embeds, images = [header_messages[category].embed], [header_messages[category].image]
        embeds.extend([tutorial_message.embed for tutorial_message in tutorial_messages[category]])
        images.extend([tutorial_message.image for tutorial_message in tutorial_messages[category]])
        await message_channel.send(
            embeds=embeds,
            files=images
        )
    await message_channel.send(
        embed=madam_nazar_location_message.embed,
        file=madam_nazar_location_message.image
    )
    logging.info("Данные о дейликах успешно отображены!")


@tasks.loop(time=config.LAUNCH_TIME)
async def scheduled_publish():
    await daily_challenges_guide()


@client.slash_command(description="Ручная публикация гайдов по дейликам")
@application_checks.has_permissions(administrator=True)
async def daily_challenges(interaction: nextcord.Interaction):
    if interaction.channel.id == config.TARGET_CHANNEL_ID:
        await interaction.response.send_message(
            embed=nextcord.Embed(
                description="✅ _Публикация начинается!_",
                colour=nextcord.Color.from_rgb(*config.BASIC_COLOR_CODE)), ephemeral=True
        )
        await daily_challenges_guide()
    else:
        await interaction.response.send_message(
            embed=nextcord.Embed(
                title="Ошибка",
                description="❌ _Публикация гайдов по дейликам вне специального канала не допускается!_",
                colour=nextcord.Color.red()), ephemeral=True
        )


@client.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        await interaction.response.send_message(
            embed=nextcord.Embed(
                title="Ошибка",
                description="Публиковать гайды по дейликам могут только администраторы.",
                colour=nextcord.Color.red()), ephemeral=True
        )
    else:
        logging.error(f"При использовании команды произошла непредвиденная ошибка: {error}")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
    if not scheduled_publish.is_running():
        scheduled_publish.start()
