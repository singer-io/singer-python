import sys
import json
import os
import logging
import logging.config

from collections import namedtuple


def _writeline(s):
    sys.stdout.write(s + '\n')
    sys.stdout.flush()


def write_record(stream_name, record):
    """Write a single record for the given stream.

    >>> write_record("users", {"id": 2, "email": "mike@stitchdata.com"})
    """
    _writeline(json.dumps({'type': 'RECORD',
                           'stream': stream_name,
                           'record': record}))


def write_records(stream_name, records):
    """Write a list of records for the given stream.

    >>> chris = {"id": 1, "email": "chris@stitchdata.com"}
    >>> mike = {"id": 2, "email": "mike@stitchdata.com"}
    >>> write_records("users", [chris, mike])
    """
    for record in records:
        write_record(stream_name, record)


def write_schema(stream_name, schema, key_properties):
    """Write a schema message.

    >>> stream = 'test'
    >>> schema = {'properties': {'id': {'type': 'integer'}, 'email': {'type': 'string'}}}  # nopep8
    >>> key_properties = ['id']
    >>> write_schema(stream, schema, key_properties)
    """
    if isinstance(key_properties, (str, bytes)):
        key_properties = [key_properties]
    if not isinstance(key_properties, list):
        raise Exception("key_properties must be a string or list of strings")
    _writeline(json.dumps({'type': 'SCHEMA',
                           'stream': stream_name,
                           'key_properties': key_properties,
                           'schema': schema}))


def write_state(value):
    """Write a state message.

    >>> write_state({'last_updated_at': '2017-02-14T09:21:00'})
    """
    _writeline(json.dumps({'type': 'STATE',
                           'value': value}))


def get_logger():
    """Return a Logger instance appropriate for using in a Tap or a Target."""
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    return logging.getLogger('root')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
