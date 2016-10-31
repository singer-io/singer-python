import sys

from transit.writer import Writer
from io import StringIO

_headers_written = False

def _writeline(s):
    print(s)
    sys.stdout.flush()

def _write_headers():
    global _headers_written
    if not _headers_written:
        _writeline('stitchstream/0.1')
        _writeline('Content-Type: transit')
        _writeline('--')
        _headers_written = True

def write_records(stream_name, key_fields, records):
    _write_headers()
    for record in records:
        s = StringIO()
        writer = Writer(s, "json")
        writer.write({'type': 'RECORD',
                      'stream': stream_name,
                      'key_fields': key_fields,
                      'record': record})
        _writeline(s.getvalue().strip())

def write_bookmark(value):
    _write_headers()
    s = StringIO()
    writer = Writer(s, "json")
    writer.write({'type': 'BOOKMARK',
                  'value': value})
    _writeline(s.getvalue().strip())


if __name__ == "__main__":
    write_records('test', ['a'], [{'a': 'b'}, {'c':'d'}])
