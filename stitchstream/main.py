import sys
import json
from io import StringIO
import os
import logging
import logging.config

def _writeline(s):
    sys.stdout.write(s + '\n')
    sys.stdout.flush()

def write_records(stream_name, records):
    for record in records:
        _writeline(json.dumps({'type': 'RECORD',
                               'stream': stream_name,
                               'record': record}))

def write_schema(stream_name, schema):
    _writeline(json.dumps({'type': 'SCHEMA',
                           'stream': stream_name,
                           'schema': schema}))

def write_state(value):
    _writeline(json.dumps({'type': 'STATE',
                           'value': value}))


def get_logger():
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    return logging.getLogger('root')

    
if __name__ == "__main__":
    write_schema('test',
                 {'properties':{'id': {'type': 'string', 'key': True}}})
    write_records('test',
                  [{'id': 'b'}, {'id':'d'}])
