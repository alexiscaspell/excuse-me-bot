import threading
import sys
from platform import python_version

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from config.configuration import CurrentConfig
from services import bot_service
from utils import system_util
from utils.carga_dinamica_blue_prints import registrar_blue_prints
from utils.logger_util import get_logger

app_name = 'ExcuseMeBot'

system_util.set_logger(get_logger("system_util"))

app = Flask(app_name)
app.config.from_object('config.configuration.CurrentConfig')
CORS(app)
logger = get_logger(app_name)

registrar_blue_prints(app,"api/v1")

@app.route("/alive")
def alive():
    return jsonify(success=True, msg="Host: " + str(system_util.SystemMonitor.ip())+":"+str(CurrentConfig.API_PORT))

if __name__ == '__main__':

    possible_ports = [int(CurrentConfig.API_PORT),80,5000]
    bot_service.init(CurrentConfig.TELEGRAM_TOKEN)
    bot_service.run()

    for port in possible_ports:
        try:
            app.run(debug=CurrentConfig.DEBUG, host=CurrentConfig.API_HOST, port=port,threaded=True)
            break
        except:
            continue

