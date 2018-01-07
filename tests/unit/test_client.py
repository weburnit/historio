import historio.client as client
from historio import Model
import unittest
import mock
import historio.definition.api_pb2 as api_pb2


class ClientTest(unittest.TestCase):
    def setUp(self):
        super(ClientTest, self).setUp()
        self.logger = mock.MagicMock()
        self.client = client.historio(server='localhost', port=5505, ignore_error=False, logger=self.logger)

    def test_singleton(self):
        grpc = client.historio(server='localhost', port=5505, ignore_error=False)
        new = client.historio()

        self.assertEqual(grpc, new)

    def test_decorate(self):
        """
        :type stub_client: mock | historio.definition.api_pb2_grpc.HistoryServiceStub
        :param stub_client: client mock
        :return:
        """
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True):
            @client.historio(user_id='Paul', action="update", source='assignment_test_decorate',
                               source_id='source_id_test_decorate',
                               server='localhost',
                               port=5555)
            def test_my_decorate():
                return {'name': 'Paul', 'age': 20}

            grpc = client.historio().client()
            test_my_decorate()
            grpc.push.assert_called_once()
            grpc.reset_mock()

    @mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True)
    def test_decorate_function_within_params(self):
        """
        :type stub_client: mock | historio.definition.api_pb2_grpc.HistoryServiceStub
        :param stub_client: client mock
        :return:
        """
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True):
            @client.historio(user_id='Paul',
                               action="update",
                               source='assignment',
                               source_id='source_id',
                               server='localhost',
                               port=5555)
            def test_my_decorate(name):
                return {'name': name, 'age': 20}

            grpc = client.historio().client()
            test_my_decorate('paul')
            grpc.push.assert_called_once()
            grpc.reset_mock()

    @mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True)
    def test_decorate_by_class(self):
        """
        :type stub_client: mock | historio.definition.api_pb2_grpc.HistoryServiceStub
        :param stub_client: client mock
        :return:
        """
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True):
            @client.historio(server='localhost', port=5555)
            def test_my_decorate():
                class MyClassInDecorate(Model):
                    def __init__(self, id):
                        self.id = id

                    def source(self):
                        return 'assignment'

                    def get_data(self):
                        return {'name': 'Paul', 'age': 32,
                                'family': {'sister': 'm.Gorretti', 'brother': 'Peter', 'relative': []}}

                    def source_id(self):
                        return self.id

                return MyClassInDecorate('unique_id_from_idb')

            test_my_decorate()
            grpc = client.historio().client()
            grpc.push.assert_called_once()
            grpc.reset_mock()

    @mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True)
    def test_decorate_by_implement_historio_model(self):
        """
        :type stub_client: mock | historio.definition.api_pb2_grpc.HistoryServiceStub
        :param stub_client: client mock
        :return:
        """
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True):
            @client.historio(source='assignment',
                               action="create",
                               source_id='source_id',
                               user_id='Paul',
                               server='localhost',
                               port=5555)
            def test_my_decorate():
                class MyClassInDecorate(object):
                    name = None
                    age = 20

                    def __init__(self, name, age):
                        self.name = name
                        self.age = age

                return MyClassInDecorate('Jonathan', 20)

            test_my_decorate()
            grpc = client.historio().client()
            grpc.push.assert_called_once()
            grpc.reset_mock()

    def test_push_manually(self):
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.MagicMock(), create=True):
            client.historio().push({'name': 'Paul', 'something': 'data'},
                                     user_id='user_id',
                                     action="update",
                                     source='source',
                                     source_id='source_id')
        grpc = client.historio().client()
        grpc.push.assert_called()
        grpc.reset_mock()

    def test_error_during_creating_request(self):
        with self.assertRaises(Exception) as context:
            with mock.patch('historio.utils.resource_builder') as mocker:
                mocker.side_effect = Exception('Something weird happens')
                client.historio().push({'name': 'Paul', 'something': 'data'},
                                         user_id='user_id',
                                         action="update",
                                         source='source',
                                         source_id='source_id')
        grpc = client.historio().client()
        grpc.push.assert_not_called()
        grpc.reset_mock()

    @mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.Mock(), create=True)
    def test_client_has_logger(self):
        with self.assertRaises(Exception) as context:
            with mock.patch('historio.utils.resource_builder') as mocker:
                mocker.side_effect = Exception('Something weird happens')
                client.historio().push({'name': 'Paul', 'something': 'data'},
                                         user_id='user_id',
                                         action="update",
                                         source='source',
                                         source_id='source_id')

        grpc = client.historio().client()
        grpc.push.assert_not_called()
        grpc.reset_mock()
        self.logger.error.assert_called_once_with('Something weird happens')

    def test_pull(self):
        with mock.patch('historio.definition.api_pb2_grpc.HistoryServiceStub', new=mock.MagicMock(), create=True):
            grpc = client.historio().client()
            mock_response = api_pb2.ListHistories(results=[], pagination=api_pb2.Pagination(total=10, display=10))
            grpc.pull.return_value = mock_response
            grpc.reset_mock()
            result = client.historio().pull(source='source')
            assert {'pagination': {'display': 10, 'total': 10}} == result
            grpc.pull.assert_called_once()


if __name__ == '__main__':
    ClientTest('Test mocking').run()
