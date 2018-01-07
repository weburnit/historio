import unittest
import mock
from historio.core.services import HistoryService
from historio.utils import resource_builder, resource_histories_builder


class ServicesTest(unittest.TestCase):
    def test_service_push_implementation(self):
        connector = mock.Mock()
        service = HistoryService(connector)
        request = resource_builder(source='source',
                                   source_id='source_id',
                                   user_id='user_id',
                                   params={'name': 'Paul'},
                                   action="create")

        service.process(request)
        connector.create.assert_called_with(request.action,
                                            request.source,
                                            request.source_id,
                                            request.user_id,
                                            request.timestamp,
                                            {'name': 'Paul'})

    def test_service_pull_implementation(self):
        connector = mock.Mock()
        service = HistoryService(connector)
        request = resource_histories_builder(source='source',
                                             source_id='source_id',
                                             user_id='user_id',
                                             display=10,
                                             page=1)

        list_of_items = [mock.Mock(), mock.MagicMock]
        connector.find_by.return_value = list_of_items
        connector.aggregation_total.return_value = 10
        result, total = service.pull(request)
        connector.find_by.assert_called_with(source='source',
                                             source_id='source_id',
                                             user_id='user_id',
                                             limit=10,
                                             page=1)

        connector.aggregation_total.assert_called_with(source=request.query.source,
                                                       source_id=request.query.source_id,
                                                       user_id=request.query.user_id,
                                                       limit=10,
                                                       page=1)
        assert (list_of_items, 10) == (result, total)
