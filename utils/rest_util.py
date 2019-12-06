from utils.logger_util import get_logger
from model.exception import AppException
from flask import abort, Flask, request,jsonify
from functools import wraps
import os
from config.configuration import CurrentConfig

def wrap_rest_response(ok: int = 200, error: int = 500, logger=get_logger(__name__)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            http_status = ok
            result = {}

            try:
                result = func(*args, **kwargs)

            except AppException as ae:

                logger.exception(ae)
                result,http_status = ae.generate_response()
            except Exception as ex:
                result = {}
                logger.exception(ex)
                http_status = 500

            return jsonify(result=get_valid_rest_object(result)), http_status
            # return jsonify(result=result), http_status
        return wrapper
    return decorator

def get_valid_rest_object(some_result):
    if not some_result:
        return some_result
    elif isinstance(some_result,list):
        return [get_valid_rest_object(e) for e in some_result]
    elif isinstance(some_result,dict):
        return some_result
    elif hasattr(some_result.__class__, 'to_dict') and callable(getattr(some_result.__class__, 'to_dict')):
        return some_result.to_dict()
    else:
        return some_result

