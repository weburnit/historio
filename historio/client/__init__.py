"""historio Client"""
import grpc
from historio.definition import api_pb2_grpc
import historio.utils as utils
from logging import Logger
from google.protobuf import json_format


class historio(object):
    """
    historio Client to push history record
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Args:
            server: refers to historio service address
            port: as its name
            ignore_error: bool as handling error or not
            logger: refers to logger instance which reflects logging.Logger
        :type logger: logging.Logger
        :param logger: Logger
        :type ignore_error: str
        :param ignore_error: Denote that you want to catch exception
        """
        if historio._instance is None:
            historio._instance = historio._Singleton(kwargs)

        historio._instance.init_params(kwargs)
        return historio._instance

    class _Singleton(object):
        """
        We ensure client must be a singleton
        """
        _grpc = None
        _action = ''
        _source = ''
        _source_id = ''
        _user_id = ''
        logger = None

        def __init__(self, params):
            """
            :type params: dict
            :param params: params
            """
            self.server = params['server']
            self.port = str(params['port'])
            self.ignore_error = True
            self.ignore_error = utils.dict_value(params, 'ignore_error', True)
            self.logger = utils.dict_value(params, 'logger', None)
            self.init_params(params)

        def init_params(self, params):
            self._source = utils.dict_value(params, 'source', self._source)
            self._source_id = utils.dict_value(params, 'source_id', self._source_id)
            self._user_id = utils.dict_value(params, 'user_id', self._user_id)
            self._action = utils.dict_value(params, 'action', self._action)

        def client(self):
            """
            Get GRPC_client
            :return: HistoryServiceStub
            """
            if not self._grpc:
                channel = grpc.insecure_channel('%s:%s' % (self.server,
                                                           self.port))
                self._grpc = api_pb2_grpc.HistoryServiceStub(channel=channel)
            return self._grpc

        def __call__(self, f):
            def wrapper(*args, **kwargs):
                action = self._action
                source = self._source
                user_id = self._user_id
                source_id = self._source_id
                result = f(*args, **kwargs)
                return self.push(result, user_id=user_id, source=source, source_id=source_id, action=action)

            return wrapper

        def pull(self, **kwargs):
            """
            :param source: Source name
            :param source_id: Source ID
            :param user_id: Source name
            :param kwargs: dic

            :return:
            """
            request = utils.resource_histories_builder(**kwargs)
            result = self.client().pull(request)

            return json_format.MessageToDict(result)

        def push(self, data, user_id, source=None, source_id=None, action="update"):
            """
            :type action: str
            :param action: Action name
            :type source: str
            :param source: Source name
            :type source_id: str
            :param source_id: Source ID as unique one to trace in history service
            :type user_id: str
            :param user_id: User ID who made this change
            :type data: dict
            :param data:
            :return:
            """
            try:
                request = utils.resource_builder(
                    source=source,
                    user_id=user_id,
                    source_id=source_id,
                    action=action,
                    params=data)
                result = self.client().push(request)
                return result
            except Exception as e:
                if self.logger:
                    self.logger.error(e.message)
                if not self.ignore_error:
                    raise

    def __call__(self, f):
        return self._instance.__call__(f)
