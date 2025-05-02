import os
import engine.troubleshooting.utils as utils
import engine.config as global_config


TROUBLESHOOTING_GUIDES_DIR = os.path.join(global_config.SOLUTIONS_DIR, 'troubleshooting')
TROUBLESHOOTING_ASSETS_DIR = os.path.join(global_config.ASSETS_DIR, 'troubleshooting')
TROUBLESHOOTING_INTRO = os.path.join(TROUBLESHOOTING_ASSETS_DIR, 'troubleshooting_intro.jpg')
TROUBLESHOOTING_SEPARATOR = os.path.join(TROUBLESHOOTING_ASSETS_DIR, 'separator_troubleshooting.jpg')
TROUBLESHOOTING_BUGS_JSON = os.path.join(TROUBLESHOOTING_GUIDES_DIR, 'bugs.json')
TROUBLESHOOTING_ERRORS_JSON = os.path.join(TROUBLESHOOTING_GUIDES_DIR, 'errors.json')
TROUBLESHOOTING_ROLE_PROBLEMS_JSON = os.path.join(TROUBLESHOOTING_GUIDES_DIR, 'role_problems.json')
TROUBLESHOOTING_TECH_ADVICES_JSON = os.path.join(TROUBLESHOOTING_GUIDES_DIR, 'tech_advices.json')

TROUBLESHOOTING_GROUPS = {
    "bugs": {
        "content": utils.json_safeload(TROUBLESHOOTING_BUGS_JSON),
        "json": TROUBLESHOOTING_BUGS_JSON
    },
    "errors": {
        "content": utils.json_safeload(TROUBLESHOOTING_ERRORS_JSON),
        "json": TROUBLESHOOTING_ERRORS_JSON
    },
    "role_problems": {
        "content": utils.json_safeload(TROUBLESHOOTING_ROLE_PROBLEMS_JSON),
        "json": TROUBLESHOOTING_ROLE_PROBLEMS_JSON
    },
    "tech_advices": {
        "content": utils.json_safeload(TROUBLESHOOTING_TECH_ADVICES_JSON),
        "json": TROUBLESHOOTING_TECH_ADVICES_JSON
    },
}
