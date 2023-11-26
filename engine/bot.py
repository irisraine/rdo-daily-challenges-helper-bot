import nextcord
from nextcord.ext import commands, tasks
import os
import datetime
from dotenv import load_dotenv
import logging
from tqdm import tqdm
import engine.config as config
import engine.messages as messages

load_dotenv()
launch_time = datetime.time(
    hour=config.DAILY_CHALLENGES_UPDATE_TIME['hour'],
    minute=config.DAILY_CHALLENGES_UPDATE_TIME['minute']
)

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = int(os.getenv('DAILY_CHALLENGES_TUTORIALS_CHANNEL'))


@tasks.loop(time=launch_time)
async def daily_challenges_guide():
    message_channel = client.get_channel(target_channel_id)
    current_date = datetime.datetime.today().strftime('%d-%m-%Y')

    header_messages = messages.get_header_messages()
    tutorial_messages = messages.get_tutorial_messages()
    madam_nazar_location_message = messages.get_madam_nazar_location_message()

    if not tutorial_messages:
        logging.error(f"Данные о дейликах за {current_date} не могут быть отображены из-за ошибки")
        return
    if not madam_nazar_location_message:
        logging.warning("Невозможно получить данные о местонахождении мадам Назар")

    progressbar = tqdm(
        desc="[PROGRESS] Размещение сообщений: ",
        total=len(range(config.OVERALL_NUMBER_OF_MESSAGES)),
        bar_format='{l_bar}{bar:25}| {n_fmt}/{total_fmt} [{elapsed}]'
    )

    await message_channel.send(
        embeds=header_messages['cover'].embeds,
        files=header_messages['cover'].images
    )
    progressbar.update(1)
    await message_channel.send(
        embeds=header_messages['general'].embeds,
        files=header_messages['general'].images
    )
    progressbar.update(1)
    for tutorial_message in tutorial_messages['general']:
        await message_channel.send(
            embeds=tutorial_message.embeds,
            files=tutorial_message.images
        )
        progressbar.update(1)
    await message_channel.send(
        embeds=header_messages['role'].embeds,
        files=header_messages['role'].images
    )
    progressbar.update(1)
    for tutorial_message in tutorial_messages['role']:
        await message_channel.send(
            embeds=tutorial_message.embeds,
            files=tutorial_message.images
        )
        progressbar.update(1)
    if madam_nazar_location_message:
        await message_channel.send(
            embeds=madam_nazar_location_message.embeds,
            files=madam_nazar_location_message.images
        )
        progressbar.update(1)
    progressbar.close()
    logging.info(f"Данные о дейликах за {current_date} успешно отображены!\n")


@client.event
async def on_ready():
    logging.info(f'Бот залогинен под именем: {client.user.name}')
    daily_challenges_guide.start()
