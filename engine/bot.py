import nextcord
from nextcord.ext import commands, tasks
import os
import datetime
from dotenv import load_dotenv
import logging
import engine.config as config
import engine.messages as messages

load_dotenv()
launch_time = datetime.time(
    hour=config.DAILY_CHALLENGES_UPDATE_TIME['hour'],
    minute=config.DAILY_CHALLENGES_UPDATE_TIME['minute']
)

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)

target_channel_id = int(os.getenv('DAILY_CHALLENGES_TUTORIALS_CHANNEL'))


async def daily_challenges_guide():
    message_channel = client.get_channel(target_channel_id)

    header_messages = messages.get_header_messages()
    tutorial_messages = messages.get_tutorial_messages()
    madam_nazar_location_message = messages.get_madam_nazar_location_message()

    if not tutorial_messages:
        logging.error("Данные о дейликах не могут быть отображены из-за ошибки\n")
        return

    await message_channel.send(
        embed=header_messages['cover'].embed,
        file=header_messages['cover'].image
    )
    for category in ('general', 'role'):
        embeds, images = [], []
        embeds.append(header_messages[category].embed)
        embeds.extend([tutorial_message.embed for tutorial_message in tutorial_messages[category]])
        images.append(header_messages[category].image)
        images.extend([tutorial_message.image for tutorial_message in tutorial_messages[category]])
        await message_channel.send(
            embeds=embeds,
            files=images
        )
    if madam_nazar_location_message:
        await message_channel.send(
            embed=madam_nazar_location_message.embed,
            file=madam_nazar_location_message.image
        )
    else:
        logging.error("Невозможно получить данные о местонахождении мадам Назар")
    logging.info("Данные о дейликах успешно отображены!")


@tasks.loop(time=launch_time)
async def scheduled_publish():
    await daily_challenges_guide()


@client.command()
@commands.has_permissions(administrator=True)
async def manual_publish(ctx):
    if ctx.channel.id == target_channel_id:
        await daily_challenges_guide()


@manual_publish.error
async def manual_publish_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Эта опция доступна только для администраторов!")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
    scheduled_publish.start()
