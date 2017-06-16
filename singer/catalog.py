'''Provides an object model for a Singer Catalog.'''

import attr
import json

from singer.schema import Schema

@attr.s
class CatalogEntry(object):
    tap_stream_id = attr.ib(default=None)
    replication_key = attr.ib(default=None)
    key_properties = attr.ib(default=None)
    schema = attr.ib(default=None)
    is_view = attr.ib(default=None)
    database = attr.ib(default=None)
    table = attr.ib(default=None)
    stream = attr.ib(default=None)
    row_count = attr.ib(default=None)

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
            result['schema'] = self.schema.to_dict() # pylint: disable=no-member
        if self.is_view is not None:
            result['is_view'] = self.is_view
        if self.stream is not None:
            result['stream'] = self.stream
        if self.row_count is not None:
            result['row_count'] = self.row_count
        return result

@attr.s
class Catalog(object):

    streams = attr.ib()
    
    def load(filename):
        with open(filename) as fp:
            return Catalog.from_dict(json.load(fp))

    @classmethod
    def from_dict(self, data):
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
