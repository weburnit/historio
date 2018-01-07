import unittest
import mock
from historio.core import HistorioServer
import time
from historio.definition import api_pb2


class ServerTest(unittest.TestCase):
    def test_push(self):
        mock_repo = mock.MagicMock()
        with mock.patch('historio.core.services.HistoryService') as services:
            with mock.patch('historio.core.connector.connect', return_value=mock_repo) as connector:
                config = {'some': 'configuration'}
                server = HistorioServer(config)
                connector.assert_called_with(configuration=config)
                services.assert_called_with(mock_repo)
                self.assertIsInstance(server, HistorioServer)

                request = mock.Mock()
                context = mock.Mock()
                server.push(request, context)
                server.historio.process.assert_called_with(request)

    def test_pull(self):
        mock_repo = mock.MagicMock()
        with mock.patch('historio.core.services.HistoryService') as services:
            with mock.patch('historio.core.connector.connect', return_value=mock_repo) as connector:
                config = {'some': 'configuration'}
                server = HistorioServer(config)
                connector.assert_called_with(configuration=config)
                services.assert_called_with(mock_repo)
                self.assertIsInstance(server, HistorioServer)

                request = api_pb2.HistoriesRequest(
                    query=api_pb2.HistoryRequest(source='source'),
                    pagination=api_pb2.Pagination(display=1)
                )
                context = mock.Mock()

                class atomic(object):
                    pass

                item = atomic()
                item.source = 'sourcing'
                item.action = 'update'
                item.source_id = 'source_id'
                item.timestamp = time.time()
                item.user_id = 'specific_user_id'
                item.metadata = {'name': 'Paul'}

                server.historio.pull.return_value = ([item, item], 10)
                result = server.pull(request, context)
                server.historio.pull.assert_called_with(request)
                self.assertIsInstance(result, api_pb2.ListHistories, "Make sure result must be proper Instance")
                self.assertEqual(2, len(result.results), "Make sure service return corresponding list")
