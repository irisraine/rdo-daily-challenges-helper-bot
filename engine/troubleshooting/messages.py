import nextcord
import engine.config as global_config
import engine.troubleshooting.config as config


class MessageContainer:
    def __init__(self, title=None, description=None, image_path=None, image_url=None):
        self.__embed = nextcord.Embed(
            title=title,
            description=description,
            colour=nextcord.Colour.from_rgb(*global_config.BASIC_COLOR_CODE),
        )
        if image_url:
            self.__embed.set_image(url=image_url)
            self.__image = None
        else:
            if not image_path:
                image_path = global_config.SEPARATOR
            image_name = image_path.replace('\\', '/').split('/')[-1]
            image_attachment = f"attachment://{image_name}"
            self.__embed.set_image(url=image_attachment)
            self.__image = nextcord.File(image_path, filename=image_name)

    @property
    def embed(self):
        return self.__embed

    @property
    def image(self):
        return self.__image


def main_menu():
    embed_message_logo = MessageContainer(
        image_path=config.TROUBLESHOOTING_INTRO
    )
    embed_message = MessageContainer(
        title="**Решение проблем с различными багами**",
        description="Данные авторские гайды содержат решение множества проблем и багов в игре Red Dead Online, а также "
                    "дополнительную полезную информацию о фичах игры.\n"
                    "Для получения помощи выберите нужную категорию из списка ниже.",
        image_path=config.TROUBLESHOOTING_SEPARATOR
    )
    return {
        'embeds': [embed_message_logo.embed, embed_message.embed],
        'files': [embed_message_logo.image, embed_message.image]
    }


def group_menu(group):
    group_data = config.TROUBLESHOOTING_GROUPS[group]["content"]
    title = group_data['title'].upper()
    description = (f"{group_data['description_header']}\n\n"
                   f"__**СОДЕРЖАНИЕ РАЗДЕЛА**__\n\n")

    categories = group_data["categories"].values()
    for category in categories:
        description += f'{category["category_emoji"]} `{category["title"]}` {category["category_emoji"]}\n'
        if group != "errors":
            for solution in category["solutions"].values():
                description += f"- *{solution['name']}*\n"
        else:
            for solution in category["solutions"].values():
                if solution['name'][1]:
                    if solution['name'][1][0] == "+":
                        description += f"- *{solution['name'][0]} {solution['name'][1]}*\n"
                    else:
                        description += f"- *{solution['name'][0]}: {solution['name'][1]}*\n"
                else:
                    description += f"- *{solution['name'][0]}*\n"
        description += "\n"

    embed_message = MessageContainer(
        title=title,
        description=description,
    )
    return {'embed': embed_message.embed, 'file': embed_message.image}


def category_menu(group, category):
    category_data = config.TROUBLESHOOTING_GROUPS[group]["content"]["categories"][category]
    title = category_data['title'].upper()
    description = (f"{category_data['description_header']}\n\n"
                   f"__**СОДЕРЖАНИЕ РАЗДЕЛА**__\n\n")

    solutions = category_data["solutions"].values()
    if group != "errors":
        for solution in solutions:
            description += f"{category_data['category_emoji']} *{solution['name']}*\n"
    else:
        for solution in solutions:
            if solution['name'][1]:
                if solution['name'][1][0] == "+":
                    description += f"{category_data['category_emoji']} *{solution['name'][0]} {solution['name'][1]}*\n"
                else:
                    description += f"{category_data['category_emoji']} *{solution['name'][0]}: {solution['name'][1]}*\n"
            else:
                description += f"{category_data['category_emoji']} *{solution['name'][0]}*\n"
    embed_message = MessageContainer(
        title=title,
        description=description,
    )
    return {'embed': embed_message.embed, 'file': embed_message.image}


def solution_guide(group, category, solution):
    solution_data = config.TROUBLESHOOTING_GROUPS[group]["content"]["categories"][category]["solutions"][solution]
    title = solution_data['title']
    description = solution_data['description']
    image_url = solution_data.get('image')

    embed_message = MessageContainer(
        title=title,
        description=description,
        image_url=image_url
    )
    return {'embed': embed_message.embed} if image_url else {'embed': embed_message.embed, 'file': embed_message.image}


def info(description, error=False):
    title = "Успешно" if not error else "Ошибка"

    embed_message = MessageContainer(
        title=title,
        description=description,
    )
    return {'embed': embed_message.embed, 'file': embed_message.image}
