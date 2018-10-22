import sys

import dateutil.parser
import pytz
import simplejson as json

import singer.utils as u

class Message():
    '''Base class for messages.'''

    def asdict(self):  # pylint: disable=no-self-use
        raise Exception('Not implemented')

    def __eq__(self, other):
        return isinstance(other, Message) and self.asdict() == other.asdict()

    def __repr__(self):
        pairs = ["{}={}".format(k, v) for k, v in self.asdict().items()]
        attrstr = ", ".join(pairs)
        return "{}({})".format(self.__class__.__name__, attrstr)

    def __str__(self):
        return str(self.asdict())


class RecordMessage(Message):
    '''RECORD message.

    The RECORD message has these fields:

      * stream (string) - The name of the stream the record belongs to.
      * record (dict) - The raw data for the record
      * version (optional, int) - For versioned streams, the version
        number. Note that this feature is experimental and most Taps and
        Targets should not need to use versioned streams.

    msg = singer.RecordMessage(
        stream='users',
        record={'id': 1, 'name': 'Mary'})

    '''

    def __init__(self, stream, record, version=None, time_extracted=None):
        self.stream = stream
        self.record = record
        self.version = version
        self.time_extracted = time_extracted
        if time_extracted and not time_extracted.tzinfo:
            raise ValueError("'time_extracted' must be either None " +
                             "or an aware datetime (with a time zone)")

    def asdict(self):
        result = {
            'type': 'RECORD',
            'stream': self.stream,
            'record': self.record,
        }
        if self.version is not None:
            result['version'] = self.version
        if self.time_extracted:
            as_utc = self.time_extracted.astimezone(pytz.utc)
            result['time_extracted'] = u.strftime(as_utc)
        return result

    def __str__(self):
        return str(self.asdict())


class SchemaMessage(Message):
    '''SCHEMA message.

    The SCHEMA message has these fields:

      * stream (string) - The name of the stream this schema describes.
      * schema (dict) - The JSON schema.
      * key_properties (list of strings) - List of primary key properties.

    msg = singer.SchemaMessage(
        stream='users',
        schema={'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'}
                }
               },
        key_properties=['id'])

    '''
    def __init__(self, stream, schema, key_properties, bookmark_properties=None):
        self.stream = stream
        self.schema = schema
        self.key_properties = key_properties

        if isinstance(bookmark_properties, (str, bytes)):
            bookmark_properties = [bookmark_properties]
        if bookmark_properties and not isinstance(bookmark_properties, list):
            raise Exception("bookmark_properties must be a string or list of strings")

        self.bookmark_properties = bookmark_properties

    def asdict(self):
        result = {
            'type': 'SCHEMA',
            'stream': self.stream,
            'schema': self.schema,
            'key_properties': self.key_properties
        }
        if self.bookmark_properties:
            result['bookmark_properties'] = self.bookmark_properties
        return result


class StateMessage(Message):
    '''STATE message.

    The STATE message has one field:

      * value (dict) - The value of the state.

    msg = singer.StateMessage(
        value={'users': '2017-06-19T00:00:00'})

    '''
    def __init__(self, value):
        self.value = value

    def asdict(self):
        return {
            'type': 'STATE',
            'value': self.value
        }


class ActivateVersionMessage(Message):
    '''ACTIVATE_VERSION message (EXPERIMENTAL).

    The ACTIVATE_VERSION messages has these fields:

      * stream - The name of the stream.
      * version - The version number to activate.

    This is a signal to the Target that it should delete all previously
    seen data and replace it with all the RECORDs it has seen where the
    record's version matches this version number.

    Note that this feature is experimental. Most Taps and Targets should
    not need to use the "version" field of "RECORD" messages or the
    "ACTIVATE_VERSION" message at all.

    msg = singer.ActivateVersionMessage(
        stream='users',
        version=2)

    '''
    def __init__(self, stream, version):
        self.stream = stream
        self.version = version

    def asdict(self):
        return {
            'type': 'ACTIVATE_VERSION',
            'stream': self.stream,
            'version': self.version
        }


def _required_key(msg, k):
    if k not in msg:
        raise Exception("Message is missing required key '{}': {}".format(k, msg))

    return msg[k]


def parse_message(msg):
    """Parse a message string into a Message object."""

    # We are not using Decimals for parsing here.
    # We recognize that exposes data to potentially
    # lossy conversions.  However, this will affect
    # very few data points and we have chosen to
    # leave conversion as is for now.
    obj = json.loads(msg)
    msg_type = _required_key(obj, 'type')

    if msg_type == 'RECORD':
        time_extracted = obj.get('time_extracted')
        if time_extracted:
            time_extracted = dateutil.parser.parse(time_extracted)
        return RecordMessage(stream=_required_key(obj, 'stream'),
                             record=_required_key(obj, 'record'),
                             version=obj.get('version'),
                             time_extracted=time_extracted)


    elif msg_type == 'SCHEMA':
        return SchemaMessage(stream=_required_key(obj, 'stream'),
                             schema=_required_key(obj, 'schema'),
                             key_properties=_required_key(obj, 'key_properties'),
                             bookmark_properties=obj.get('bookmark_properties'))

    elif msg_type == 'STATE':
        return StateMessage(value=_required_key(obj, 'value'))

    elif msg_type == 'ACTIVATE_VERSION':
        return ActivateVersionMessage(stream=_required_key(obj, 'stream'),
                                      version=_required_key(obj, 'version'))
    else:
        return None


def format_message(message):
    return json.dumps(message.asdict(), use_decimal=True)


def write_message(message):
    sys.stdout.write(format_message(message) + '\n')
    sys.stdout.flush()


def write_record(stream_name, record, stream_alias=None, time_extracted=None):
    """Write a single record for the given stream.

    write_record("users", {"id": 2, "email": "mike@stitchdata.com"})
    """
    write_message(RecordMessage(stream=(stream_alias or stream_name),
                                record=record,
                                time_extracted=time_extracted))


def write_records(stream_name, records):
    """Write a list of records for the given stream.

    chris = {"id": 1, "email": "chris@stitchdata.com"}
    mike = {"id": 2, "email": "mike@stitchdata.com"}
    write_records("users", [chris, mike])
    """
    for record in records:
        write_record(stream_name, record)


def write_schema(stream_name, schema, key_properties, bookmark_properties=None, stream_alias=None):
    """Write a schema message.

    stream = 'test'
    schema = {'properties': {'id': {'type': 'integer'}, 'email': {'type': 'string'}}}  # nopep8
    key_properties = ['id']
    write_schema(stream, schema, key_properties)
    """
    if isinstance(key_properties, (str, bytes)):
        key_properties = [key_properties]
    if not isinstance(key_properties, list):
        raise Exception("key_properties must be a string or list of strings")

    write_message(
        SchemaMessage(
            stream=(stream_alias or stream_name),
            schema=schema,
            key_properties=key_properties,
            bookmark_properties=bookmark_properties))


def write_state(value):
    """Write a state message.

    write_state({'last_updated_at': '2017-02-14T09:21:00'})
    """
    write_message(StateMessage(value=value))


def write_version(stream_name, version):
    """Write an activate version message.

    stream = 'test'
    version = int(time.time())
    write_version(stream, version)
    """
    write_message(ActivateVersionMessage(stream_name, version))
