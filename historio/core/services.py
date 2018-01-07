"""History Service which reflects business logic layer in this project"""
import json
from google.protobuf import json_format
from historio.utils import filter_dictionary


class HistoryService(object):
    """History Service which is injected in GRPC Service implementation"""

    def __init__(self, connector):
        """
        :type connector: historio.core.connector.Repository
        :param connector:
        """
        self.connector = connector

    def process(self, request):
        """
        Where we can implement GRPC business logic
        :type request: historio.definition.api_pb2.HistoryRequest
        :param request:
        :return: historio.core.models.HistoryModel
        """
        metadata = json.loads(json_format.MessageToJson(request.metadata))
        self.connector.create(request.action, request.source, request.source_id,
                              request.user_id, request.timestamp, metadata)

    def pull(self, request):
        """
        Return History data to client
        :type request: historio.definition.api_pb2.HistoryRequest
        :param request:
        :return: historio.core.models.HistoryModel, int
        """
        query = {'source': request.query.source,
                 'source_id': request.query.source_id,
                 'user_id': request.query.user_id,
                 'limit': request.pagination.display,
                 'page': request.pagination.current_page,
                 'start': int(request.pagination.start),
                 'end': int(request.pagination.end)
                 }
        query = filter_dictionary(query, [None, "", 0])
        results = self.connector.find_by(**query)
        total = self.connector.aggregation_total(**query)
        return results, total
