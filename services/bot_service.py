import json
import random
import sys

from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater

import utils.redis.redis_manager as rm
from config.configuration import (ENVIRONMENT_MODE, CurrentConfig,
                                  DevelopmentConfig, HerokuConfig)
from model.mensaje import Mensaje
from utils.logger_util import get_logger

logger = get_logger(__name__)

TOKEN=None
BOT=None

def obtener_elemento_random(una_lista):
    desde = 0
    hasta = len(una_lista)
    index =  random.randrange(desde,hasta,1)
    return una_lista[index]

def get_lista_de_redis(nombre_lista):
    try:
        return rm.get_by_key(nombre_lista,Mensaje)
    except Exception as e:
        logger.error("Fallo al obtener elemento de redis, obteniendo de json hard...",e)

    with open("backup.json","r") as f:
        return [Mensaje(e) for e in json.load(f)[nombre_lista]]

def agregar_mensaje(lista_a_agregar, message):
    lista = get_lista_de_redis(lista_a_agregar)
    lista_a_agregar.append(message)
    rm.set_by_key(lista,lista_a_agregar)

def obtener_mensaje_random():
    preposicion = obtener_elemento_random(get_lista_de_redis("preposiciones")).texto
    actor = obtener_elemento_random(get_lista_de_redis("actores")).texto.replace("...","")
    factor = obtener_elemento_random(get_lista_de_redis("factores")).texto
    return f"{preposicion} {actor} {factor}"

def excuse_me(request_body):
    enviar_menasaje_por_bot(dame_una_excusa(),request_body,reply_message=False)

def enviar_menasaje_por_bot(mensaje:str,request_body:dict={},reply_message=True):
    update = Update.de_json(request_body, BOT)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    logger.info(f"got text message : {text}")

    if reply_message:
        BOT.sendMessage(chat_id=chat_id, text=mensaje, reply_to_message_id=msg_id)
    else:
        BOT.sendMessage(chat_id=chat_id, text=mensaje)

def dame_una_excusa():
    logger.info("Negro pidiendo excusa...")
    return obtener_mensaje_random()

def setear_webhook(uri:str="/"):
    logger.info(f"Seteando webhook en {uri}")
    return BOT.set_webhook(f"{CurrentConfig.WEB_HOOK_URL}{uri}/{TOKEN}")

def run():
    # BOT.start_polling()
    global BOT
    BOT = Bot(token=TOKEN)

    logger.info("Started bot")

# def agregar_comando(nombre_func,func):
#     BOT.dispatcher.add_handler(CommandHandler(nombre_func, func))

def init(token:str):
    global TOKEN

    TOKEN = token

    logger.info("Starting bot")
    # agregar_comando("excuse_me",excuse_me)
