import logging
import os
import time

from pymongo import MongoClient
from pythonjsonlogger import jsonlogger

from historio import core

server = None
_ONE_HOUR_HEALTH_CHECK = 60*10


def logger(mod_name):
    _logging = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()

    handler.setFormatter(formatter)
    _logging.addHandler(handler)
    _logging.setLevel(logging.DEBUG)
    return _logging


_logger = logger('historio')


def health_check():
    """Health check every minutes"""
    client = MongoClient(os.environ.get('MONGO_HOST'))
    try:
        result = client.server_info()
        _logger.info(result)
    except Exception as e:
        _logger.error(e.message, exc_info=True)
        raise e


def handling_server(grpc):
    """
    :type grpc: grpc.server
    :param grpc:
    :return:
    """
    global server
    server = grpc
    try:
        while True:
            health_check()
            time.sleep(_ONE_HOUR_HEALTH_CHECK)
    except KeyboardInterrupt:
        grpc.stop(0)


PORT = os.environ.get('GRPC_PORT', 5501)
MAX_WORKER = os.environ.get('GRPC_WORKER', 10)
if __name__ == '__main__':
    _logger.info('Run historio Application')
    handling_server(core.start(PORT, MAX_WORKER))
