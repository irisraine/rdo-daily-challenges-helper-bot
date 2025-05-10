import logging


def load_cogs(client):
    cogs = ['daily_challenges', 'troubleshooting']
    for cog in cogs:
        try:
            client.load_extension(f"engine.{cog}.cog")
            logging.info(f"Модуль {cog} успешно загружен.")
        except Exception as error:
            logging.error(f"Ошибка при попытке загрузки модуля {cog}. Дополнительная информация: {error}")
