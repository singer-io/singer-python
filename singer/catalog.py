@attr.s
class CatalogEntry(object):
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
        result = {
            'database': self.database,
            'table': self.table,
        }
        if self.replication_key is not None:
            result['replication_key'] = self.replication_key
        if self.key_properties is not None:
            result['key_properties'] = self.key_properties
        if self.schema is not None:
            result['schema'] = self.schema.to_json() # pylint: disable=no-member
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
            streams.append(
                CatalogEntry(
                    replication_key=stream.get('replication_key'),
                    key_properties=stream.get('key_properties'),
                    database=stream.get('database'),
                    table=stream.get('table'),
                    schema=Schema.from_dict(stream.get('schema')),
                    is_view=stream.get('is_view')))
        return Catalog(streams)
        
        
    def to_dict(self):
        return {'streams': [stream.to_json() for stream in self.streams]}
    
    def dump(self):
        json.dump(self.to_dict(), sys.stdout, indent=2)
