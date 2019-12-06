import os
from logging import INFO,ERROR,WARNING,DEBUG
import sys


class HerokuConfig():
    DEBUG = False
    OUTPUT_FILES_FOLDER = 'output/'
    API_HOST = os.environ.get("PYTHON_HOST", "0.0.0.0")
    API_PORT =  int(os.environ.get('PORT', 80))
    API_BASE_PATH = "/api"
    LOG_LEVELS = [INFO,ERROR]
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
    REDIS_HOST = os.environ.get("REDIS_HOST", "0.0.0.0")
    REDIS_PASSWD = os.environ.get("REDIS_PASSWD", None)
    REDIS_URL = os.environ.get("REDIS_URL",None)
    HEROKU_APP_NAME = None
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN",None)


class DevelopmentConfig():
    DEBUG = True
    OUTPUT_FILES_FOLDER = 'output/'
    API_HOST = os.environ.get("PYTHON_HOST", "0.0.0.0")
    API_PORT =  int(os.environ.get('PORT', 5000))
    API_BASE_PATH = "/api"
    LOG_LEVELS = [INFO,ERROR,WARNING,DEBUG]
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
    REDIS_HOST = os.environ.get("REDIS_HOST", "0.0.0.0")
    REDIS_PASSWD = os.environ.get("REDIS_PASSWD", None)
    REDIS_URL = os.environ.get("REDIS_URL",None)
    HEROKU_APP_NAME = None
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN",None)

def is_environment_param():
    return len(sys.argv)>1 and str(sys.argv) in ["development"]

class_config_name = str(sys.argv[1]) if is_environment_param() else os.environ.get("ENVIRONMENT_MODE", "development")
class_config_name = class_config_name.title()+"Config"

CurrentConfig = getattr(sys.modules[__name__], f"{class_config_name}")()

# CurrentConfig = ProductionConfig()
