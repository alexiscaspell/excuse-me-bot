from flask import (Blueprint, jsonify, request)
from utils.logger_util import get_logger
from flask_cors import CORS, cross_origin
from config.configuration import CurrentConfig
from utils.rest_util import wrap_rest_response
from model.mensaje import Mensaje
from services import bot_service

logger = get_logger(__name__)
blue_print = Blueprint('bot', __name__,
                     url_prefix=CurrentConfig.API_BASE_PATH+'/v1/bot')


@cross_origin
@blue_print.route("/mensajes", methods=['POST'])
@wrap_rest_response(ok=200, logger=logger)
def agregar_factor():
    """Agrega un mensaje de factores"""

    body = request.get_json(force=True)

    lista_a_agregar = body["lista"]

    message = Mensaje(body)

    bot_service.agregar_mensaje(lista_a_agregar, message)

@blue_print.route(f'/{CurrentConfig.TELEGRAM_TOKEN}', methods=['POST'])
@wrap_rest_response(ok=200, logger=logger)
def respond():
    body = request.get_json(force=True)

    logger.info(f"MSG:{body}")

    bot_service.excuse_me(body)

    return 'ok'

@blue_print.route('/run', methods=['GET'])
@wrap_rest_response(ok=200, logger=logger)
def run():
    
    bot_service.init(CurrentConfig.TELEGRAM_TOKEN)
    bot_service.run()
    bot_service.setear_webhook(uri=blue_print.url_prefix)

    return 'ok'