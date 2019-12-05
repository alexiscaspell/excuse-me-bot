from telegram.ext import Updater, CommandHandler
import requests
import re
import random

TOKEN = "1060592042:AAHrBpp4AVN8jugVTlW0Rl7s7Veq0USdcwI"

preposiciones = ["I'm sorry but... ","Please forgive MC...","Beg you a thousand pardons...","I apologize, however...","I'm never usually like this...","You're never going to believe this...","Guess what happened?!?...","Holy. shit! Get this...","I swear it wasn't my fault...","My bad...","Boy do I have a story for you...","So I was minding my own business and boom!...","most unbelievable thing just happened...","I couldn't be more apologetic but...","Sorry I'm late,.I couldn't go because...","I couldn't help it...","This is a terrible excuse but...","This is going to sound crazy but...","Holy Moses!. ","Blimey Sorry I'm late guv'nha","I lost track of time because..."]
actores = ["McCallisters real", "Kevin Costner's stunt double...", "Kevin Spacey...", "a hasidic Jew...", "a British chap...", "Kevin Ware's leg bone...", "the entire Roman Empire...", "Ghost Dad...", "the ghost of Hitler...", "the ghost of Margaret Thatcher...", "Scrooge McDuck...", "Mayor McCheese...", "your mom...", "Princess Peach...", "Godzilla...", "the offensive of 76 Dallas Cowboys...", "a handicapped gentleman...", "a triceratops named Penelope...", "the director of 101 Dalmations...", "the little Asian kid from Indiana Jones...", "a man nith 6 fingers on his right hand...", "Raiders from Mortal ", "your mom..."]
factores = ["ran me over with a diesel backhoe.",                                     "died in front of ME",                                     "ate my homework.",                                     "tried to seduce me.",                                     "heat me into submission.",                                     "hid my Trapper Keeper.",                                     "stole my bicycle.",                                     "slept with my uncle.",                                     "called me 'too gay to fly a kite', whatever that means.",                                     "stole my identity.",                                     "broke into my house.",                                     "put me in a Chinese finger trap.",                                     "came after me.",                                     "came on me.",                                     "texted racial shin from my phone.",                                     "spin-kicked me in the collar bone.",                                     "tried to sell me vacuum cleaners.",                                     "trapped in my gas tank.",                                     "made me golf in shoes",                                     "filled with macaroni and cheese.",                                     "pulled me over in a stolen",                                     "cop car and demanded fellatio.",                                     "made me find Jesus.",                                     "tried to kill me.",                                     "gave me a hickey."]


def obtener_elemento_random(una_lista):
    desde = 0
    hasta = len(una_lista)
    index =  random.randrange(desde,hasta,1)
    return una_lista[index]

# def get_url():
#     contents = requests.get('https://random.dog/woof.json').json()    
#     url = contents['url']
#     return url

def obtener_mensaje_random():
    preposicion = obtener_elemento_random(preposiciones)
    actor = obtener_elemento_random(actores).replace("...","")
    factor = obtener_elemento_random(factores)
    return f"{preposicion} {actor} {factor}"

def excuse_me(bot, update):
    mensaje = obtener_mensaje_random()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=mensaje)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('excuse_me',excuse_me))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
