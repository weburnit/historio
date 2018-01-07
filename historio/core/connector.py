"""historio Connector deal with DB layer"""
from historio.core.models import HistoryModel
from historio.utils import dict_value, filter_key
from mongoengine import connect as mongo_connector


def connect(configuration):
    """
    :type configuration: dict
    :param configuration: Configuration
    :rtype: Repository
    :return: Repository
    """
    database = dict_value(configuration, 'database', 'inspector_history')
    host = dict_value(configuration, 'host', 'mongo')
    port = dict_value(configuration, 'port')
    username = dict_value(configuration, 'username')
    password = dict_value(configuration, 'password')
    mongo_connector(host=host, db=database, port=port,
                    username=username, password=password)
    return Repository()


class Repository(object):
    """Define Behavior for service Layer to deal with Model"""

    @staticmethod
    def create(action, source, source_id, user_id, timestamp, metadata):
        instance = HistoryModel(source=source,
                                source_id=source_id,
                                user_id=user_id,
                                timestamp=timestamp,
                                metadata=metadata,
                                action=action)
        instance.save()
        return instance

    @staticmethod
    def find(source_id):
        """
        :type source_id: str
        :param source_id: Source ID
        :rtype: HistoryModel
        :return: HistoryModel
        """
        return HistoryModel.objects(source_id=source_id).first()

    @staticmethod
    def find_by(*args, **kwargs):
        """Find a collection"""
        limit = dict_value(kwargs, 'limit', 20)
        page = int(dict_value(kwargs, 'page', 1))
        if args and isinstance(args[0], dict):
            kwargs = args[0]
            args = []
        if 'start' in kwargs:
            kwargs['timestamp__gte'] = kwargs['start']
        if 'end' in kwargs:
            kwargs['timestamp__lte'] = kwargs['end']
        filter_query = filter_key(kwargs, ['limit', 'page', 'start', 'end'])
        return HistoryModel.objects(*args, **filter_query).skip((page - 1) * limit).limit(limit)

    @staticmethod
    def aggregation_total(*args, **kwargs):
        """Aggregate pagination for one single request"""
        filter_query = filter_key(kwargs, ['limit', 'page'])
        return HistoryModel.objects(*args, **filter_query).count()
