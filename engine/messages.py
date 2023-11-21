import nextcord
import requests
import os
import json
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from engine.api_handler import get_daily_challenges_api_response, get_madam_nazar_location_map_url
import engine.config as config

basic_color = nextcord.Colour.from_rgb(*config.BASIC_COLOR_CODE)
newline = "\n"
role_titles = {
    'bounty_hunter': f'{config.EMOJI["bounty_hunter_emoji"]} Охотник за головами',
    'naturalist': f'{config.EMOJI["naturalist_emoji"]} Натуралист',
    'trader': f'{config.EMOJI["trader_emoji"]} Торговец',
    'collector': f'{config.EMOJI["collector_emoji"]} Коллекционер',
    'moonshiner': f'{config.EMOJI["moonshiner_emoji"]} Самогонщик'
}


class TutorialMessage:
    def __init__(self, title=None, description=None, image_path=None):
        self.__embed = nextcord.Embed(
            title=title,
            description=description,
            colour=basic_color
        )
        if not image_path:
            image_path = config.SEPARATOR
        image_name = image_path.split('/')[-1]
        image_attachment = f'attachment://{image_name}'
        self.__embed.set_image(url=image_attachment)
        filepath = os.path.join(os.getcwd(), image_path)
        self.__image = nextcord.File(filepath, filename=image_name)

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


def get_description(index, solutions, current_challenge):
    task = f"{index + 1}. {solutions[current_challenge['title']]['task']}: "
    goal = f"`0/{current_challenge['goal']}`"
    solution = f"{solutions[current_challenge['title']]['solution']}"
    description = f'***{task}{goal}***{solution}'
    return description


def get_header_messages():
    today = datetime.today()
    current_date_formatted = f"{today.day} {config.MONTH_LIST[today.month - 1]} {today.year}"
    header_cover_image_blank_path = os.path.join(os.getcwd(), config.HEADER_COVER_BLANK)
    font_path = os.path.join(os.getcwd(), config.CUSTOM_RDO_FONT)
    cover_image = Image.open(header_cover_image_blank_path)
    draw = ImageDraw.Draw(cover_image)
    font = ImageFont.truetype(font_path, size=200)
    image_length, text_length = 1280, int(draw.textlength(current_date_formatted, font))
    x_shift, y_shift = ((image_length - text_length) // 2), 500
    draw.text((x_shift, y_shift), current_date_formatted, fill='white', font=font,
              stroke_width=4, stroke_fill='black')
    cover_image.save(config.HEADER_COVER)

    header_messages = {
        'cover': TutorialMessage(image_path=config.HEADER_COVER),
        'general': TutorialMessage(image_path=config.HEADER_GENERAL),
        'role': TutorialMessage(image_path=config.HEADER_ROLE)
    }
    return header_messages


def get_madam_nazar_location_message():
    madam_nazar_location_map_url = get_madam_nazar_location_map_url()
    response = requests.get(madam_nazar_location_map_url)
    location_filepath = os.path.join(os.getcwd(), config.MADAM_NAZAR_LOCATION_MAP)
    with open(location_filepath, 'wb') as file:
        file.write(response.content)
    title = f"{config.EMOJI['madam_nazar_emoji']} Мадам Назар: <t:{int(datetime.now().timestamp())}:D>"
    description = "Сегодняшнее местонахождение мадам Назар вы можете увидеть на карте, приведенной ниже:"
    madam_nazar_location_message = TutorialMessage(
        title=title,
        description=description,
        image_path=location_filepath
    )
    return madam_nazar_location_message


def get_tutorial_messages():
    daily_challenges_api_response = get_daily_challenges_api_response()
    if not daily_challenges_api_response:
        return None
    general_tutorial_messages = []
    role_tutorial_messages = []
    for category in config.CATEGORIES:
        if category == 'general':
            solutions = get_solutions(category)
            if not solutions:
                return None
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description = get_description(index, solutions, current_challenge)
                image = solutions[current_challenge['title']]['image']
                image_path = os.path.join(os.getcwd(), image) if image else None
                message = TutorialMessage(description=description, image_path=image_path)
                general_tutorial_messages.append(message)
        else:
            solutions = get_solutions(category)
            if not solutions:
                return None
            title = f"**{role_titles[category]}**"
            description = ""
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description_single = get_description(index, solutions, current_challenge)
                description += f"{description_single}{newline}"
            message = TutorialMessage(title=title, description=description)
            role_tutorial_messages.append(message)
    tutorial_messages = {
        'general': general_tutorial_messages,
        'role': role_tutorial_messages
    }
    return tutorial_messages
