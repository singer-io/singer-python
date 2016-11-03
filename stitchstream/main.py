import sys
import json
from io import StringIO

_headers_written = False

def _writeline(s):
    print(s)
    sys.stdout.flush()

def _write_headers():
    global _headers_written
    if not _headers_written:
        _writeline('stitchstream/0.1')
        _writeline('Content-Type: jsonline')
        _writeline('--')
        _headers_written = True

def write_records(stream_name, schema, records):
    _write_headers()
    for record in records:
        _writeline(json.dumps({'type': 'RECORD',
                               'stream': stream_name,
                               'schema': schema,
                               'record': record}))

def write_bookmark(value):
    _write_headers()
    _writeline(json.dumps({'type': 'BOOKMARK',
                           'value': value}))


if __name__ == "__main__":
    write_records('test',
                  {'properties':{'id': {'type': 'string', 'key': True}}},
                  [{'id': 'b'}, {'id':'d'}])
