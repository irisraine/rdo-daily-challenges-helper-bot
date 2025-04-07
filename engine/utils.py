import os
import requests
import logging
from datetime import time


def get_response_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            response.raise_for_status()
    except requests.exceptions.Timeout:
        logging.error(f"{url} не отвечает")
        return
    except (requests.RequestException, requests.HTTPError):
        logging.error(f"Ошибка соединения с {url}")
        return


def get_time_object(hour=0, minute=0):
    return time(hour=hour, minute=minute)


def get_file_path(*dirs, filename):
    file_path = os.path.join(*dirs, filename)
    if not os.path.isfile(file_path):
        logging.error(f'Файл {filename} отсутствует, проверьте правильность пути!')
        return None
    return file_path
