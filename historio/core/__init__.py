"""GRPC Server bootstrap"""
import os
from concurrent import futures
import grpc
from historio.core import connector, services
from historio.definition import api_pb2_grpc, api_pb2
from historio.utils import resource_builder, parse_struct
from google.protobuf import struct_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

CONFIG = {
    'host': os.environ.get('MONGO_HOST', 'localhost'),
    'database': os.environ.get('MONGO_DB', 'historio'),
    'port': int(os.environ.get('MONGO_PORT', 27017)),
    'username': os.environ.get('MONGO_USER', 'historio'),
    'password': os.environ.get('MONGO_PASS', '$1$IaGjCYU'),
}
stop = False


def start(port, max_workers=10):
    """Start Server"""
    grpc_server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=max_workers))  # pragma: no cover
    api_pb2_grpc.add_HistoryServiceServicer_to_server(HistorioServer(CONFIG), grpc_server)  # pragma: no cover
    grpc_server.add_insecure_port('[::]:' + str(port))  # pragma: no cover
    grpc_server.start()  # pragma: no cover
    return grpc_server  # pragma: no cover


class HistorioServer(api_pb2_grpc.HistoryServiceServicer):
    """Impelement GRPC Server"""

    def __init__(self, config):
        super(HistorioServer, self).__init__()
        repository = connector.connect(configuration=config)
        self.historio = services.HistoryService(repository)

    def push(self, request, context):
        """
        Implement function PUSH defined by api.proto
        :param request:
        :param context:
        :return:
        """
        self.historio.process(request)
        return api_pb2.BaseResponse(status=True)

    def pull(self, request, context):
        """
        @TODO Implement API return historical instances from Mongodb
        :param request:
        :param context:
        :return:
        """
        results, total = self.historio.pull(request)
        histories = []
        for item in results:
            result = resource_builder(item.metadata,
                                      item.source,
                                      item.source_id,
                                      item.user_id,
                                      item.action)
            histories.append(result)

        pagination = api_pb2.Pagination(total=total,
                                        display=request.pagination.display,
                                        current_page=request.pagination.current_page)

        return api_pb2.ListHistories(results=histories, pagination=pagination)
