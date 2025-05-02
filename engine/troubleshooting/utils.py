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


def validate_json_structure(new_json_data):
    try:
        required_top_keys = {'title', 'description_header', 'select_menu_placeholder', 'emoji', 'categories'}
        if not all(key in new_json_data for key in required_top_keys):
            return False

        if not all(isinstance(new_json_data[key], str) for key in
                   ['title', 'description_header', 'select_menu_placeholder', 'emoji']):
            return False

        if not isinstance(new_json_data['categories'], dict) or not new_json_data['categories']:
            return False

        for category, category_data in new_json_data['categories'].items():
            required_category_keys = {'title', 'description_header', 'category_emoji', 'solutions'}
            if not all(key in category_data for key in required_category_keys):
                return False

            if not all(isinstance(category_data[key], str) for key in ['title', 'description_header', 'category_emoji']):
                return False

            if not isinstance(category_data['solutions'], dict) or not category_data['solutions']:
                return False

            if len(category_data['solutions']) > 25:
                return False

            for solution, solution_data in category_data['solutions'].items():
                required_solution_keys = {'name', 'title', 'description'}
                if not all(key in solution_data for key in required_solution_keys):
                    return False

                if not (isinstance(solution_data['name'], (str, list)) and
                        isinstance(solution_data['title'], str) and
                        isinstance(solution_data['description'], str)):
                    return False
        return True

    except Exception as error:
        logging.error(f"Произошла ошибка '{error}' при попытке чтения переданного файла! Изменения не сохранены.")
        return False
