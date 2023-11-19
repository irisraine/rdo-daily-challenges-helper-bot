import nextcord
import time
import requests
import os
import json
import logging
from engine.api_handler import get_daily_challenges, get_madam_nazar_location
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


def get_solutions(category):
    filename = os.path.join(os.getcwd(), "solutions", f'{category}.json')
    if not os.path.isfile(filename):
        logging.warning(f'Файл с туториалами {filename} отсутствует, проверьте правильность пути!')
        return None
    with open(filename, 'r') as file:
        return json.load(file)


def get_complete_text(index, current_solutions, current_challenge):
    description_text = f"{index + 1}. {current_solutions[current_challenge['title']]['description']}: "
    goal_text = f"`0/{current_challenge['goal']}`"
    solution_text = f"* {current_solutions[current_challenge['title']]['solution']}"
    complete_text = f"**{description_text}{goal_text}**{newline}{solution_text}"
    return complete_text


def get_embed(complete_text, image=None):
    message = nextcord.Embed(
        description=complete_text,
        colour=basic_color)
    if not image:
        image = config.SEPARATOR
    is_image_exists = requests.get(image)
    if is_image_exists:
        message.set_image(url=image)
    else:
        logging.warning(f'Ссылка {image} не работает!')
    return message


def get_initial_message():
    initial_message = nextcord.Embed(
        title=f"ДЕЙЛИКИ НА <t:{int(time.time())}:D>",
        colour=basic_color)
    return initial_message


def get_general_title_message():
    general_title_message = nextcord.Embed(
        title=f'{config.EMOJI["pointer_emoji"]} '
              f'Общие ежедневные задания '
              f'{config.EMOJI["pointer_emoji"]}',
        colour=basic_color)
    return general_title_message


def get_role_title_message():
    role_title_message = nextcord.Embed(
        title=f'{config.EMOJI["pointer_emoji"]} '
              f'Ролевые ежедневные задания '
              f'{config.EMOJI["pointer_emoji"]}',
        colour=basic_color)
    return role_title_message


def get_madam_nazar_message():
    location = get_madam_nazar_location()
    if not location:
        return None
    madam_nazar_message = nextcord.Embed(
        title=f'{config.EMOJI["madam_nazar_emoji"]} '
              f'Мадам Назар: <t:{int(time.time())}:D>',
        description="Сегодняшнее местонахождение мадам Назар вы можете увидеть на карте, приведенной ниже:",
        colour=basic_color)
    madam_nazar_message.set_image(url=location)
    return madam_nazar_message


def get_daily_challenges_messages():
    daily_challenges = get_daily_challenges()
    if not daily_challenges:
        return None
    daily_challenges_general_messages = []
    daily_challenges_roles_messages = []
    for category in config.CATEGORIES:
        if category == 'general':
            current_solutions = get_solutions(category)
            if not current_solutions:
                return None
            for i, current_challenge in enumerate(daily_challenges[category]):
                complete_text = get_complete_text(i, current_solutions, current_challenge)
                image = current_solutions[current_challenge['title']]['image']
                message = get_embed(complete_text, image)
                daily_challenges_general_messages.append(message)
        else:
            current_solutions = get_solutions(category)
            if not current_solutions:
                return None
            complete_text = f"**{role_titles[category]}**{newline}"
            for i, current_challenge in enumerate(daily_challenges[category]):
                complete_text += (f"{newline}"
                                  f"{get_complete_text(i, current_solutions, current_challenge)}"
                                  f"{newline}")
            message = get_embed(complete_text)
            daily_challenges_roles_messages.append(message)
    daily_challenges_messages = {
        'general': daily_challenges_general_messages,
        'roles': daily_challenges_roles_messages
    }
    return daily_challenges_messages
