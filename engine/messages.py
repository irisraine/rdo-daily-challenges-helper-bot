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
    def __init__(self, title=None, description=None, images_paths=None):
        self.__embeds = []
        self.__images = []
        main_embed = nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Colour.from_rgb(*config.BASIC_COLOR_CODE),
        )
        self.__embeds.append(main_embed)
        if not images_paths:
            images_paths = [config.SEPARATOR]
        if len(images_paths) > 1:
            self.__embeds[0].url = config.DUMMY_LINK
            linking_embed = nextcord.Embed(url=config.DUMMY_LINK)
            self.__embeds.append(linking_embed)
        for index, image_path in enumerate(images_paths):
            image_name = image_path.split('/')[-1]
            image_attachment = f'attachment://{image_name}'
            self.__embeds[index].set_image(url=image_attachment)
            filepath = os.path.join(os.getcwd(), image_path)
            image_file = nextcord.File(filepath, filename=image_name)
            self.__images.append(image_file)

    @property
    def embeds(self):
        return self.__embeds

    @property
    def images(self):
        return self.__images


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
    header_cover_image_blank_path = os.path.join(os.getcwd(), config.HEADER_COVER_BLANK)
    font_path = os.path.join(os.getcwd(), config.CUSTOM_RDO_FONT)
    cover_image = Image.open(header_cover_image_blank_path)
    draw = ImageDraw.Draw(cover_image)
    font = ImageFont.truetype(font_path, size=200)
    image_length, text_length = 1280, int(draw.textlength(current_date_formatted, font))
    x_shift, y_shift = ((image_length - text_length) // 2), 500
    draw.text((x_shift, y_shift), current_date_formatted, fill='white', font=font,
              stroke_width=10, stroke_fill='black')
    cover_image.save(config.HEADER_COVER)

    header_messages = {
        'cover': MessageContainer(images_paths=[config.HEADER_COVER]),
        'general': MessageContainer(images_paths=[config.HEADER_GENERAL]),
        'role': MessageContainer(images_paths=[config.HEADER_ROLE])
    }
    return header_messages


def get_madam_nazar_location_message():
    madam_nazar_location = get_madam_nazar_location_api_response()
    if not madam_nazar_location:
        return None
    image_path = get_image_path(f'{config.MADAM_NAZAR_LOCATION_MAPS_DIR}/{madam_nazar_location}.jpg')
    if not image_path:
        return None
    title = f"{config.EMOJI['madam_nazar_emoji']} Мадам Назар: <t:{int(datetime.now().timestamp())}:D>"
    madam_nazar_location_message = MessageContainer(
        title=title,
        images_paths=[image_path]
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
                images = solutions[current_challenge['title']]['images']
                images_paths = []
                for image in images:
                    image_path = get_image_path(image)
                    images_paths.append(image_path)
                message = MessageContainer(description=description, images_paths=images_paths)
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
            message = MessageContainer(title=title, description=description)
            role_tutorial_messages.append(message)
    tutorial_messages = {
        'general': general_tutorial_messages,
        'role': role_tutorial_messages
    }
    return tutorial_messages
