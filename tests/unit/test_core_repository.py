import unittest
from mongoengine import connect
import historio.core.connector as connector
from historio.core.models import HistoryModel
import time
from unittest_data_provider import data_provider
import mock

timing = str(time.time())


class CoreRepositoryTest(unittest.TestCase):
    repository = None
    request_cases = lambda: (
        ({'source': 'minor_resource', 'source_id': 'source_id_%s' % timing, 'start': timing},
         {'source': 'minor_resource', 'source_id': 'source_id_%s' % timing, 'user_id': 'user_id'}),
        ({'source': 'source_%s' % timing, 'end': timing},
         {'source': 'source_%s' % timing, 'source_id': 'source_id_%s' % timing, 'user_id': 'user_id'}),
        ({'source': 'source_%s' % timing, 'user_id': 'some_user_id'},
         {'source': 'source_%s' % timing, 'source_id': 'source_id_%s' % timing, 'user_id': 'some_user_id'})
    )

    def setUp(self):
        super(CoreRepositoryTest, self).setUp()
        connect('mongoenginetest', host='mongomock://localhost')
        self.repository = connector.Repository()

    def test_connect(self):
        import historio.core.connector as connector_test
        with mock.patch('mongoengine.connect') as mocker:
            result = connector_test.connect(
                {'host': 'localhost', 'port': 27017, 'database': 'test_db', 'username': 'root', 'password': 'pass'})
            self.assertIsInstance(result, connector.Repository)

    def test_create(self):
        document = self.repository.create('create', 'source', 'source_id', 'user_id', float(timing), {'name': 'Paul'})
        self.assertIsInstance(document, HistoryModel)

    def test_find(self):
        document = self.repository.create('create', 'source', 'source_id', 'user_id', float(timing), {'name': 'Paul'})
        result = self.repository.find(document.source_id)
        assert result.source_id == document.source_id

    def test_find_by(self):
        source_id = 'source_id_%s' % (str(time.time()))
        document = self.repository.create('create', 'source', source_id, 'user_id',
                                          float(timing), {'name': 'Paul'})
        result = self.repository.find_by(source_id=source_id)
        assert result.first().source_id == document.source_id
        assert result.first().source == document.source

    def test_find_by_two_items(self):
        source_id = 'source_id_%s' % (str(time.time()))
        self.repository.create('create', 'source', source_id, 'user_id',
                               float(timing), {'name': 'Paul'})
        self.repository.create('create', 'source', source_id, 'user_id',
                               float(timing), {'name': 'Jonathan'})
        result = self.repository.find_by(source_id=source_id)
        assert len(result) == 2

    @data_provider(request_cases)
    def test_find_by_request(self, request, created_item):
        self.repository.create('create', created_item['source'], created_item['source_id'], created_item['user_id'],
                               float(timing), {'name': 'Paul'})
        result = self.repository.find_by(request)
        assert result.first().source == created_item['source']

    def test_find_by_dictionary(self):
        self.repository.create('create', 'source_aggregate', 'source_id_aggregate_1', 'user_id_aggregate_1',
                               float(timing), {'name': 'Paul'})
        self.repository.create('create', 'source_aggregate', 'source_id_aggregate_2', 'user_id_aggregate_2',
                               float(timing), {'name': 'Paul'})
        query = {'source': u"source", "limit": 1}
        result = self.repository.find_by(**query)
        assert len(result) == 1
        query = {'source': u"source", "limit": 2}
        result = self.repository.find_by(**query)
        assert len(result) == 2

    def test_aggregate_count(self):
        self.repository.create('create', 'source_aggregate', 'source_id_aggregate_1', 'user_id_aggregate_1',
                               float(timing), {'name': 'Paul'})
        self.repository.create('create', 'source_aggregate', 'source_id_aggregate_2', 'user_id_aggregate_2',
                               float(timing), {'name': 'Paul'})
        result = self.repository.aggregation_total(source='source_aggregate')
        assert result == 2
