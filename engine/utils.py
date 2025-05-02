import logging


def load_cogs(client):
    cogs = ['engine.daily_challenges.cog', 'engine.troubleshooting.cog']
    for cog in cogs:
        try:
            client.load_extension(cog)
            logging.info(f"Модуль {cog.split('.')[1]} успешно загружен.")
        except Exception as error:
            logging.error(f"Ошибка при попытке загрузки модуля '{cog.split('.')[-1]}'. "
                          f"Дополнительная информация: {error}")
