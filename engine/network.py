import requests
import logging


def get_response_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logging.info(f"Ответ от {url} успешно получен!")
            return response.content
        else:
            response.raise_for_status()
    except (requests.RequestException, requests.HTTPError):
        logging.error(f"Ошибка соединения с {url}")
        return None
    except requests.exceptions.Timeout:
        logging.error(f"{url} не отвечает")
        return None
