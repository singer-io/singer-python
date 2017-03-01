import sys
import json
import os
import logging
import logging.config

import attr


class Message(object):
    def tojson(self):
        return json.dumps(attr.asdict(self))


@attr.s
class RecordMessage(Message):
    stream = attr.ib()
    record = attr.ib()
    type = attr.ib(default="RECORD")


@attr.s
class SchemaMessage(Message):
    stream = attr.ib()
    schema = attr.ib()
    key_properties = attr.ib()
    type = attr.ib(default="SCHEMA")


@attr.s
class StateMessage(Message):
    value = attr.ib()
    type = attr.ib(default="STATE")


def _write_message(message):
    sys.stdout.write(message.tojson() + '\n')
    sys.stdout.flush()


def write_record(stream_name, record):
    """Write a single record for the given stream.

    >>> write_record("users", {"id": 2, "email": "mike@stitchdata.com"})
    """
    _write_message(RecordMessage(stream=stream_name, record=record))


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
    _write_message(
        SchemaMessage(
            stream=stream_name,
            schema=schema,
            key_properties=key_properties))


def write_state(value):
    """Write a state message.

    >>> write_state({'last_updated_at': '2017-02-14T09:21:00'})
    """
    _write_message(StateMessage(value=value))


def _required_key(msg, k):
    if k not in msg:
        raise Exception("Message is missing required key '{}': {}".format(
            k, msg))
    return msg[k]


def parse_message(s):
    """Parse a message string into a Message object."""
    o = json.loads(s)
    t = _required_key(o, 'type')

    if t == 'RECORD':
        return RecordMessage(_required_key(o, 'stream'),
                             _required_key(o, 'record'))

    elif t == 'SCHEMA':
        return SchemaMessage(_required_key(o, 'stream'),
                             _required_key(o, 'schema'),
                             _required_key(o, 'key_properties'))

    elif t == 'STATE':
        return StateMessage(_required_key(o, 'value'))


def get_logger():
    """Return a Logger instance appropriate for using in a Tap or a Target."""
    this_dir, this_filename = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    return logging.getLogger('root')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
