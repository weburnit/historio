import logging
import time
from google.protobuf import struct_pb2
from historio.definition import api_pb2
from historio import Model
from google.protobuf import json_format
import json


def dict_value(source, key, default=None):
    if key in source:
        return source[key]
    return default


l = logging.getLogger('dict_to_protbuf')

__all__ = ['dict_to_protobuf']


def parse_list(values, message):
    '''parse list to protobuf message'''
    if isinstance(values[0], dict):  # value needs to be further parsed
        for v in values:
            cmd = message.add()
            parse_dict(v, cmd)
    else:  # value can be set
        message.extend(values)


def parse_dict(values, message):
    for k, v in values.iteritems():
        if isinstance(v, dict):  # value needs to be further parsed
            parse_dict(v, getattr(message, k))
        elif isinstance(v, list):
            parse_list(v, getattr(message, k))
        else:  # value can be set
            try:
                setattr(message, k, v)
            except AttributeError:
                logging.basicConfig()
                l.warning('try to access invalid attributes %r.%r = %r', message, k, v)


def parse_null(data):
    if isinstance(data, (bytearray, list, tuple)) and len(data) == 0:
        return None
    return data


def parse_struct(values, message):
    if isinstance(values, dict):
        values = json.loads(json.dumps(values, default=parse_null))
        json_format.ParseDict(values, message)


def dict_to_protobuf(value, message):
    parse_dict(value, message)


def resource_builder(params, user_id, source, source_id, action):
    """
    :param source: Source name regarding to history model such as "assignment", "inspection", "settings"
    :param source_id: source unique ID refer to source
    :param action: Action ["create","update","delete"]
    :param user_id: User Id refers to user ID
    :param params:
    :return: Request Instance
    :rtype: api_pb2.HistoryRequest
    """

    if isinstance(params, Model):
        source = params.source()
        source_id = params.source_id()
        params = params.get_data()
    return _resource_model_builder(params, user_id, source, source_id, action)


def resource_histories_builder(**kwargs):
    """Build Histories Request
    :return: api_pb2.HistoriesRequest
    """
    query = {'source': dict_value(kwargs, 'source', None),
             'source_id': dict_value(kwargs, 'source_id', None),
             'user_id': dict_value(kwargs, 'user_id', None)}
    request = api_pb2.HistoryRequest(**filter_dictionary(query))
    pagination = {'display': dict_value(kwargs, 'display', 10),
                  'current_page': dict_value(kwargs, 'page', 1),
                  'total': dict_value(kwargs, 'total', None),
                  'start': float(dict_value(kwargs, 'start', 0)),
                  'end': float(dict_value(kwargs, 'end', 0))}

    return api_pb2.HistoriesRequest(query=request, pagination=filter_dictionary(pagination))


def filter_dictionary(request, ignore=[None, ""]):
    """
    Filter None and empty string in dictionary
    :param ignore: list
    :param request: dict
    :return: dict
    """
    if isinstance(request, dict):
        return {k: v for k, v in request.iteritems() if v not in ignore}
    return request


def filter_key(request, keys):
    """
    Remove some keys in dictionary
    :param request:
    :param keys: Key would be removed
    :return: dict
    """
    if isinstance(request, dict):
        return {k: v for k, v in request.iteritems() if k not in keys}
    return request


def _resource_model_builder(params, user_id, source, source_id, action):
    """Build Request"""
    timestamp = time.time()
    metadata = struct_pb2.Struct()
    parse_struct(params, metadata)
    request = api_pb2.HistoryRequest(source=source, user_id=user_id, source_id=source_id, timestamp=timestamp,
                                     metadata=metadata, action=action)
    return request
