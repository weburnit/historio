"""Model reflects history Mongo Collection"""
from mongoengine import StringField, FloatField, DictField, DynamicDocument


class HistoryModel(DynamicDocument):
    """History Collection"""
    action = StringField(required=True, max_length=64)
    source = StringField(required=True, max_length=64)
    source_id = StringField(required=True, max_length=64)
    user_id = StringField(required=True, max_length=64)
    timestamp = FloatField(required=True)
    metadata = DictField()
    meta = {
        'indexes': [
            'source',
            'source_id',
            'user_id',
            'timestamp'
        ]
    }
