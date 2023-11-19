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

target_channel_id = int(os.getenv('DAILY_TUTORIALS_CHANNEL'))


@tasks.loop(minutes=1)
async def daily_challenges_guide():
    message_channel = client.get_channel(target_channel_id)

    daily_challenges_messages = messages.get_daily_challenges_messages()
    if not daily_challenges_messages:
        logging.warning(f"Данные о дейликах за {datetime.today().strftime('%d-%m-%Y')} не отображены из-за ошибки")
    else:
        await message_channel.send(embed=messages.get_initial_message())
        await message_channel.send(embed=messages.get_general_title_message())
        await message_channel.send(embeds=daily_challenges_messages['general'])
        await message_channel.send(embed=messages.get_role_title_message())
        await message_channel.send(embeds=daily_challenges_messages['roles'])
        try:
            await message_channel.send(embed=messages.get_madam_nazar_message())
        except nextcord.errors.HTTPException:
            logging.warning(f"Невозможно получить данные о местонахождении мадам Назар")
        logging.info(f"Данные о дейликах за {datetime.today().strftime('%d-%m-%Y')} успешно отображены")


@client.event
async def on_ready():
    logging.info(f'Залогинен под именем: {client.user.name}')
    daily_challenges_guide.start()


