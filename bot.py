import os
import sys
from logger_util import get_logger
from telegram.ext import Updater, CommandHandler
import requests
import re
import random


logger = get_logger(__name__)

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE","dev")
TOKEN = os.getenv("TOKEN")
preposiciones = ["I'm sorry but... ","Please forgive MC...","Beg you a thousand pardons...","I apologize, however...","I'm never usually like this...","You're never going to believe this...","Guess what happened?!?...","Holy. shit! Get this...","I swear it wasn't my fault...","My bad...","Boy do I have a story for you...","So I was minding my own business and boom!...","most unbelievable thing just happened...","I couldn't be more apologetic but...","Sorry I'm late,.I couldn't go because...","I couldn't help it...","This is a terrible excuse but...","This is going to sound crazy but...","Holy Moses!. ","Blimey Sorry I'm late guv'nha","I lost track of time because..."]
actores = ["McCallisters real", "Kevin Costner's stunt double...", "Kevin Spacey...", "a hasidic Jew...", "a British chap...", "Kevin Ware's leg bone...", "the entire Roman Empire...", "Ghost Dad...", "the ghost of Hitler...", "the ghost of Margaret Thatcher...", "Scrooge McDuck...", "Mayor McCheese...", "your mom...", "Princess Peach...", "Godzilla...", "the offensive of 76 Dallas Cowboys...", "a handicapped gentleman...", "a triceratops named Penelope...", "the director of 101 Dalmations...", "the little Asian kid from Indiana Jones...", "a man nith 6 fingers on his right hand...", "Raiders from Mortal ", "your mom..."]
factores = ["ran me over with a diesel backhoe.",                                     "died in front of ME",                                     "ate my homework.",                                     "tried to seduce me.",                                     "heat me into submission.",                                     "hid my Trapper Keeper.",                                     "stole my bicycle.",                                     "slept with my uncle.",                                     "called me 'too gay to fly a kite', whatever that means.",                                     "stole my identity.",                                     "broke into my house.",                                     "put me in a Chinese finger trap.",                                     "came after me.",                                     "came on me.",                                     "texted racial shin from my phone.",                                     "spin-kicked me in the collar bone.",                                     "tried to sell me vacuum cleaners.",                                     "trapped in my gas tank.",                                     "made me golf in shoes",                                     "filled with macaroni and cheese.",                                     "pulled me over in a stolen",                                     "cop car and demanded fellatio.",                                     "made me find Jesus.",                                     "tried to kill me.",                                     "gave me a hickey."]

if mode == "dev":
    def run(updater):
        logger.info("Starting DEV")
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        logger.info("Starting PROD")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
        logger.info("Webhooks setteds")
else:
    logger.error("No MODE specified!")
    sys.exit(1)



def obtener_elemento_random(una_lista):
    desde = 0
    hasta = len(una_lista)
    index =  random.randrange(desde,hasta,1)
    return una_lista[index]

def obtener_mensaje_random():
    preposicion = obtener_elemento_random(preposiciones)
    actor = obtener_elemento_random(actores).replace("...","")
    factor = obtener_elemento_random(factores)
    return f"{preposicion} {actor} {factor}"

def excuse_me(bot, update):
    logger.info("Negro pidiendo excusa...")
    mensaje = obtener_mensaje_random()
    logger.info("Viendo a quien excusar...")
    chat_id = update.message.chat_id
    logger.info("Enviando excusa...")
    bot.send_message(chat_id=chat_id, text=mensaje)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("excuse_me", excuse_me))

    run(updater)