import nextcord
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from engine.daily_challenges.content import get_daily_challenges_api_response, get_madam_nazar_location_api_response
import engine.config as global_config
import engine.daily_challenges.config as config
import engine.daily_challenges.utils as utils


ROLE_TITLES = {
    'bounty_hunter': '<:1bnf:1133866938599211048> Охотник за головами',
    'naturalist': '<:1ek:1132954387589894225> Натуралист',
    'trader': '<:1bh:1129141191326310440> Торговец',
    'collector': '<:1ao:1133012204527034418> Коллекционер',
    'moonshiner': '<:1bq:1132755527479345232> Самогонщик'
}
MONTH_LIST = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


class MessageContainer:
    def __init__(self, title=None, description=None, image_path=None, image_index=None):
        self.__embed = nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Colour.from_rgb(*global_config.BASIC_COLOR_CODE),
        )
        if not image_path:
            image_path = global_config.SEPARATOR
            image_name = f"separator_{image_index}.png"
        else:
            image_name = image_path.replace('\\', '/').split('/')[-1]
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


def get_header_messages():
    today = datetime.today()
    current_date_formatted = f"{today.day} {MONTH_LIST[today.month - 1]} {today.year}"
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
        return
    image_path = utils.get_file_path(
        config.DAILY_CHALLENGES_SOLUTIONS_IMAGES_DIR, config.MADAM_NAZAR_LOCATION_MAPS_DIR,
        filename=f'{madam_nazar_location_api_response[4:]}.jpg')
    if not image_path:
        return
    title = f"<:1bng:1133866931783475230> Мадам Назар: <t:{int(datetime.now().timestamp())}:D>"
    madam_nazar_location_message = MessageContainer(title=title, image_path=image_path)
    return madam_nazar_location_message


def get_tutorial_messages():
    daily_challenges_api_response = get_daily_challenges_api_response()
    if not daily_challenges_api_response:
        return
    general_tutorial_messages = []
    role_tutorial_messages = []
    for count, category in enumerate(config.CATEGORIES):
        solutions = _get_solutions(category)
        if not solutions:
            return
        if category == 'general':
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description = _get_description(index, solutions, current_challenge)
                image_filename = solutions[current_challenge['title']]['image']
                image_path = utils.get_file_path(
                    config.DAILY_CHALLENGES_SOLUTIONS_IMAGES_DIR,
                    filename=image_filename) if image_filename else None
                message = MessageContainer(description=description, image_path=image_path, image_index=index + 1)
                general_tutorial_messages.append(message)
        else:
            title = f"**{ROLE_TITLES[category]}**"
            description = ""
            for index, current_challenge in enumerate(daily_challenges_api_response[category]):
                description_single = _get_description(index, solutions, current_challenge)
                description += f"{description_single}\n"
            message = MessageContainer(title=title, description=description, image_index=count)
            role_tutorial_messages.append(message)
    tutorial_messages = {
        'general': general_tutorial_messages,
        'role': role_tutorial_messages
    }
    return tutorial_messages


def _get_solutions(category):
    file_path = utils.get_file_path(config.DAILY_CHALLENGES_SOLUTIONS_DIR, filename=f'{category}.json')
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


def _get_description(index, solutions, current_challenge):
    task = f"{index + 1}. {solutions[current_challenge['title']]['task']}: "
    goal = f"`0/{current_challenge['goal']}`"
    solution = f"{solutions[current_challenge['title']]['solution']}"
    description = f'***{task}{goal}***{solution}'
    return description
