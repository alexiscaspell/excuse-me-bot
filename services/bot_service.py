from telegram.ext import Updater, CommandHandler
from telegram import Bot,Update
from config.configuration import CurrentConfig,HerokuConfig,DevelopmentConfig
import utils.redis.redis_manager as rm
from utils.logger_util import get_logger
import json

logger = get_logger(__name__)

TOKEN=None
UPDATER=None

def obtener_elemento_random(una_lista):
    desde = 0
    hasta = len(una_lista)
    index =  random.randrange(desde,hasta,1)
    return una_lista[index]

def get_lista_de_redis(nombre_lista):
    try:
        return rm.get_by_key(nombre_lista,Mensaje)
    except Exception as e:
        logger.error("Fallo al obtener elemento de redis, obteniendo de json hard...")

    with open("backup.json","r") as f:
        return json.load(f)[nombre_lista]

def agregar_mensaje(lista_a_agregar, message):
    lista = get_lista_de_redis(lista_a_agregar)
    lista_a_agregar.append(message)
    rm.set_by_key(lista,lista_a_agregar)

def obtener_mensaje_random():
    preposicion = obtener_elemento_random(get_lista_de_redis("preposiciones"))
    actor = obtener_elemento_random(get_lista_de_redis("actores")).replace("...","")
    factor = obtener_elemento_random(get_lista_de_redis("factores"))
    return f"{preposicion} {actor} {factor}"

def excuse_me(bot:Bot, update:Update):
    logger.info("Negro pidiendo excusa...")
    mensaje = obtener_mensaje_random()
    logger.info("Viendo a quien excusar...")
    chat_id = update.message.chat_id
    logger.info("Enviando excusa...")
    bot.send_message(chat_id=chat_id, text=mensaje)

def run():
    if CurrentConfig==DevelopmentConfig:
        logger.info("Starting DEV mode")
        updater.start_polling()
    elif CurrentConfig==HerokuConfig:
        PORT = int(CurrentConfig.API_PORT)
        HEROKU_APP_NAME = CurrentConfig.HEROKU_APP_NAME
        logger.info("Starting HEROKU mode")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        logger.info("Webhooks setteds")
    else:
        logger.error("No MODE specified!")
        sys.exit(1)

def agregar_comando(nombre_func,func):
    updater.dispatcher.add_handler(CommandHandler(nombre_func, func))

def init(token:str):
    global updater
    global TOKEN

    TOKEN = token

    logger.info("Starting bot")
    
    updater = Updater(TOKEN)

    agregar_comando("excuse_me",excuse_me)

    run(updater)