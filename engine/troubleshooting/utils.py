import json
import os
import logging
import tempfile


def json_safeload(filepath):
    if not os.path.isfile(filepath):
        logging.error(f"Произошла ошибка при попытке открытия файла '{filepath}'! Файл не найден.")
        return
    try:
        with open(filepath, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке открытия файла '{filepath}'! Работа бота невозможна")


def json_safewrite(filepath, data):
    dir_name = os.path.dirname(filepath)
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=dir_name, delete=False) as temp_jsonfile:
            temp_jsonfile_name = temp_jsonfile.name
            json.dump(data, temp_jsonfile, ensure_ascii=False, indent=4)
        os.replace(temp_jsonfile_name, filepath)
        return True
    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке записи файла '{filepath}'! Изменения не сохранены.")
        if os.path.exists(temp_jsonfile_name):
            os.remove(temp_jsonfile_name)
        return False


def validate_json_structure(json_data):
    try:
        required_top_keys = {'title', 'description_header', 'select_menu_placeholder', 'emoji', 'categories'}
        if not all(key in json_data for key in required_top_keys):
            return 1, "Отсутствуют некоторые из необходимых ключей верхнего уровня."

        if not all(isinstance(json_data[key], str) for key in
                   ['title', 'description_header', 'select_menu_placeholder', 'emoji']):
            return 1, "Некорректный тип данных в ключах верхнего уровня. Данные должны быть строкой."

        if not isinstance(json_data['categories'], dict) or not json_data['categories']:
            return 1, "Раздел 'categories' имеет неверный тип данных. Он должен быть словарем."

        for category, category_data in json_data['categories'].items():
            required_category_keys = {'title', 'description_header', 'category_emoji', 'solutions'}
            if not all(key in category_data for key in required_category_keys):
                return 1, "Отсутствуют некоторые из необходимых ключей уровня категорий."

            if not all(isinstance(category_data[key], str) for key in ['title', 'description_header', 'category_emoji']):
                return 1, "Некорректный тип данных в ключах уровня категорий. Данные должны быть строкой."

            if not isinstance(category_data['solutions'], dict) or not category_data['solutions']:
                return 1, "Раздел 'solutions' должен быть словарем. Он должен быть словарем."

            if len(category_data['solutions']) > 25:
                return 1, "Число решений в одном разделе превышает лимит в 25 штук."

            for solution, solution_data in category_data['solutions'].items():
                required_solution_keys = {'name', 'title', 'description'}
                if not all(key in solution_data for key in required_solution_keys):
                    return 1, "Отсутствуют некоторые из необходимых ключей уровня решений."

                if not (isinstance(solution_data['name'], (str, list)) and
                        isinstance(solution_data['title'], str) and
                        isinstance(solution_data['description'], str)):
                    return 1, ("Некорректный тип данных в ключах верхнего уровня. Данные должны быть строкой, а также "
                               "допускается тип список для заголовков вопросов.")

                if not 0 < len(solution_data['name']) < 100:
                    return 1, "Длина заголовка вопроса превысила лимит в 100 символов, либо заголовок пуст."

                if len(solution_data['description']) > 4096:
                    return 1, "Длина текста с решением превышает лимит в 4096 символов."
        return 0, "Данные имеют корректный формат и содержимое."

    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке чтения переданного файла! Изменения не сохранены.")
        return 2, "Произошла ошибка при попытке чтения переданного файла."
