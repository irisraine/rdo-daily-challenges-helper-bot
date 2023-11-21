import nextcord
from nextcord.ext import commands, tasks
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
import engine.messages as messages

load_dotenv()

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = int(os.getenv('DAILY_CHALLENGES_TUTORIALS_CHANNEL'))


@tasks.loop(minutes=1)
async def daily_challenges_guide():
    message_channel = client.get_channel(target_channel_id)
    current_date = datetime.today().strftime('%d-%m-%Y')

    header_messages = messages.get_header_messages()
    tutorial_messages = messages.get_tutorial_messages()
    madam_nazar_location_message = messages.get_madam_nazar_location_message()
    if not tutorial_messages:
        logging.error(f"Данные о дейликах за {current_date} не отображены из-за ошибки")
    else:
        await message_channel.send(
            embed=header_messages['cover'].embed,
            file=header_messages['cover'].image
        )
        await message_channel.send(
            embed=header_messages['general'].embed,
            file=header_messages['general'].image
        )
        for tutorial_message in tutorial_messages['general']:
            await message_channel.send(
                embed=tutorial_message.embed,
                file=tutorial_message.image
            )
        await message_channel.send(
            embed=header_messages['role'].embed,
            file=header_messages['role'].image
        )
        for tutorial_message in tutorial_messages['role']:
            await message_channel.send(
                embed=tutorial_message.embed,
                file=tutorial_message.image
            )
        if not madam_nazar_location_message:
            logging.warning("Невозможно получить данные о местонахождении мадам Назар")
        else:
            await message_channel.send(
                embed=madam_nazar_location_message.embed,
                file=madam_nazar_location_message.image
            )
        logging.info(f"Данные о дейликах за {current_date} успешно отображены")


@client.event
async def on_ready():
    logging.info(f'Залогинен под именем: {client.user.name}')
    daily_challenges_guide.start()
