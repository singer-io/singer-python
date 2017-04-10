import sys
import json
import os
import logging
import logging.config

from singer import utils
from singer import transform

class Message(object):
    attr_list = []
    _type = None
    def __init__(self, **kwargs):
        for k in self.attr_list:
            if k not in kwargs:
                raise ValueError("missing {}".format(k))
            setattr(self, k, kwargs[k])

    def asdict(self):
        res = {k: getattr(self, k) for k in self.attr_list}
        res['type'] = self._type
        return res

    def __eq__(self, other):
        return self.asdict() == other.asdict()

    def __repr__(self):
        attrstr = ", ".join(
            "{}={}".format(k, getattr(self, k)) for k in self.attr_list)
        return "{}({})".format(self.__class__.__name__, attrstr)

    def tojson(self):
        return json.dumps(self.asdict())


class RecordMessage(Message):
    _type = 'RECORD'
    attr_list = ['stream', 'record']


class SchemaMessage(Message):
    _type = 'SCHEMA'
    attr_list = ['stream', 'schema', 'key_properties']


class StateMessage(Message):
    _type = 'STATE'
    attr_list = ['value']


def write_message(message):
    sys.stdout.write(message.tojson() + '\n')
    sys.stdout.flush()


def write_record(stream_name, record):
    """Write a single record for the given stream.

    >>> write_record("users", {"id": 2, "email": "mike@stitchdata.com"})
    """
    write_message(RecordMessage(stream=stream_name, record=record))


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
    write_message(
        SchemaMessage(
            stream=stream_name,
            schema=schema,
            key_properties=key_properties))


def write_state(value):
    """Write a state message.

    >>> write_state({'last_updated_at': '2017-02-14T09:21:00'})
    """
    write_message(StateMessage(value=value))


def _required_key(msg, k):
    if k not in msg:
        raise Exception("Message is missing required key '{}': {}".format(
            k, msg))
    return msg[k]


def parse_message(msg):
    """Parse a message string into a Message object."""
    obj = json.loads(msg)
    msg_type = _required_key(obj, 'type')

    if msg_type == 'RECORD':
        return RecordMessage(stream=_required_key(obj, 'stream'),
                             record=_required_key(obj, 'record'))

    elif msg_type == 'SCHEMA':
        return SchemaMessage(stream=_required_key(obj, 'stream'),
                             schema=_required_key(obj, 'schema'),
                             key_properties=_required_key(obj, 'key_properties'))

    elif msg_type == 'STATE':
        return StateMessage(value=_required_key(obj, 'value'))


def get_logger():
    """Return a Logger instance appropriate for using in a Tap or a Target."""
    this_dir, _ = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    return logging.getLogger('root')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
