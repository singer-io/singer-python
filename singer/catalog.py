'''Provides an object model for a Singer Catalog.'''

import json
import sys

from singer.schema import Schema


# pylint: disable=too-many-instance-attributes
class CatalogEntry(object):

    def __init__(self, tap_stream_id=None, stream=None,
                 key_properties=None, schema=None, replication_key=None,
                 is_view=None, database=None, table=None, row_count=None):

        self.tap_stream_id = tap_stream_id
        self.stream = stream
        self.key_properties = key_properties
        self.schema = schema
        self.replication_key = replication_key
        self.is_view = is_view
        self.database = database
        self.table = table
        self.row_count = row_count

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def is_selected(self):
        return self.schema.selected  # pylint: disable=no-member

    def to_dict(self):
        result = {}
        if self.tap_stream_id:
            result['tap_stream_id'] = self.tap_stream_id
        if self.database:
            result['database_name'] = self.database
        if self.table:
            result['table_name'] = self.table
        if self.replication_key is not None:
            result['replication_key'] = self.replication_key
        if self.key_properties is not None:
            result['key_properties'] = self.key_properties
        if self.schema is not None:
            schema = self.schema.to_dict()  # pylint: disable=no-member
            result['schema'] = schema
        if self.is_view is not None:
            result['is_view'] = self.is_view
        if self.stream is not None:
            result['stream'] = self.stream
        if self.row_count is not None:
            result['row_count'] = self.row_count
        return result


class Catalog(object):

    def __init__(self, streams):
        self.streams = streams

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def load(cls, filename):
        with open(filename) as fp:  # pylint: disable=invalid-name
            return Catalog.from_dict(json.load(fp))

    @classmethod
    def from_dict(cls, data):
        streams = []
        for stream in data['streams']:
            entry = CatalogEntry()
            entry.tap_stream_id = stream.get('tap_stream_id')
            entry.stream = stream.get('stream')
            entry.replication_key = stream.get('replication_key')
            entry.key_properties = stream.get('key_properties')
            entry.database = stream.get('database_name')
            entry.table = stream.get('table_name')
            entry.schema = Schema.from_dict(stream.get('schema'))
            entry.is_view = stream.get('is_view')
            streams.append(entry)
        return Catalog(streams)

    def to_dict(self):
        return {'streams': [stream.to_dict() for stream in self.streams]}

    def dump(self):
        json.dump(self.to_dict(), sys.stdout, indent=2)
