import nextcord
import os
import json
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from engine.api_handler import get_daily_challenges_api_response, get_madam_nazar_location_api_response
import engine.config as config

role_titles = {
    'bounty_hunter': f'{config.EMOJI["bounty_hunter_emoji"]} Охотник за головами',
    'naturalist': f'{config.EMOJI["naturalist_emoji"]} Натуралист',
    'trader': f'{config.EMOJI["trader_emoji"]} Торговец',
    'collector': f'{config.EMOJI["collector_emoji"]} Коллекционер',
    'moonshiner': f'{config.EMOJI["moonshiner_emoji"]} Самогонщик'
}


class MessageContainer:
    def __init__(self, title=None, description=None, image_path=None, image_index=None):
        self.__embed = nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Colour.from_rgb(*config.BASIC_COLOR_CODE),
        )
        if not image_path:
            image_path = config.SEPARATOR
            image_name = f"separator_{image_index}.png"
        else:
            image_name = image_path.split('/')[-1]
            if image_index:
                image_name = f"{image_name.split('.')[0]}_{image_index}.jpg"
        image_attachment = f"attachment://{image_name}"
        self.__embed.set_image(url=image_attachment)
        self.__image = nextcord.File(image_path, filename=image_name)

    @property
    def embed(self):
        return self.__embed

    @property
    def image(self):
        return self.__image


def get_solutions(category):
    filename = os.path.join(os.getcwd(), "solutions", f'{category}.json')
    if not os.path.isfile(filename):
        logging.error(f'Файл с туториалами {filename} отсутствует, проверьте правильность пути!')
        return None
    with open(filename, 'r') as file:
        return json.load(file)


def get_image_path(local_path):
    image_path = os.path.join(os.getcwd(), local_path)
    if not os.path.isfile(image_path):
        logging.error(f'Файл с картинкой {image_path} отсутствует, проверьте правильность пути!')
        return None
    return image_path


def get_description(index, solutions, current_challenge):
    task = f"{index + 1}. {solutions[current_challenge['title']]['task']}: "
    goal = f"`0/{current_challenge['goal']}`"
    solution = f"{solutions[current_challenge['title']]['solution']}"
    description = f'***{task}{goal}***{solution}'
    return description


def get_header_messages():
    today = datetime.today()
    current_date_formatted = f"{today.day} {config.MONTH_LIST[today.month - 1]} {today.year}"
    cover_image = Image.open(config.HEADER_COVER_BLANK)
    draw = ImageDraw.Draw(cover_image)
    font = ImageFont.truetype(config.CUSTOM_RDO_FONT, size=190)
    image_length, text_length = 1280, int(draw.textlength(current_date_formatted, font))
    x_shift, y_shift = ((image_length - text_length) // 2), 500
    draw.text((x_shift, y_shift), current_date_formatted, fill='white', font=font,
              stroke_width=10, stroke_fill='black')
    cover_image.save(config.HEADER_COVER)

    header_messages = {
        'cover': MessageContainer(image_path=config.HEADER_COVER),
        'general': MessageContainer(image_path=config.HEADER_GENERAL),
        'role': MessageContainer(image_path=config.HEADER_ROLE)
    }
    return header_messages


def get_madam_nazar_location_message():
    madam_nazar_location_api_response = get_madam_nazar_location_api_response()
    if not madam_nazar_location_api_response:
        return None
    image_path = get_image_path(f'{config.MADAM_NAZAR_LOCATION_MAPS_DIR}/{madam_nazar_location_api_response[4:]}.jpg')
    if not image_path:
        return None
    title = f"{config.EMOJI['madam_nazar_emoji']} Мадам Назар: <t:{int(datetime.now().timestamp())}:D>"
    madam_nazar_location_message = MessageContainer(title=title, image_path=image_path)
    return madam_nazar_location_message


def get_tutorial_messages():
    daily_challenges_api_response = get_daily_challenges_api_response()
    if not daily_challenges_api_response:
        return None
    general_tutorial_messages = []
    role_tutorial_messages = []
    for count, category in enumerate(config.CATEGORIES):
        if category == 'general':
            solutions = get_solutions(category)
            if not solutions:
                return None
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description = get_description(index, solutions, current_challenge)
                image = solutions[current_challenge['title']]['image']
                image_path = get_image_path(image) if image else None
                message = MessageContainer(description=description, image_path=image_path, image_index=index + 1)
                general_tutorial_messages.append(message)
        else:
            solutions = get_solutions(category)
            if not solutions:
                return None
            title = f"**{role_titles[category]}**"
            description = ""
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description_single = get_description(index, solutions, current_challenge)
                description += f"{description_single}\n"
            message = MessageContainer(title=title, description=description, image_index=count)
            role_tutorial_messages.append(message)
    tutorial_messages = {
        'general': general_tutorial_messages,
        'role': role_tutorial_messages
    }
    return tutorial_messages
