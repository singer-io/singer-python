import singer
import unittest
import datetime
import dateutil

class TestSinger(unittest.TestCase):
    def test_parse_message_record_good(self):
        message = singer.parse_message(
            '{"type": "RECORD", "record": {"name": "foo"}, "stream": "users"}')
        self.assertEqual(
            message,
            singer.RecordMessage(record={'name': 'foo'}, stream='users'))

    def test_parse_message_record_with_version_good(self):
        message = singer.parse_message(
            '{"type": "RECORD", "record": {"name": "foo"}, "stream": "users", "version": 2}')
        self.assertEqual(
            message,
            singer.RecordMessage(record={'name': 'foo'}, stream='users', version=2))

    def test_parse_message_record_naive_extraction_time(self):
        with self.assertRaisesRegex(ValueError, "must be either None or an aware datetime"):
            message = singer.parse_message(
                '{"type": "RECORD", "record": {"name": "foo"}, "stream": "users", "version": 2, "time_extracted": "1970-01-02T00:00:00"}')

    def test_parse_message_record_aware_extraction_time(self):
        message = singer.parse_message(
            '{"type": "RECORD", "record": {"name": "foo"}, "stream": "users", "version": 2, "time_extracted": "1970-01-02T00:00:00.000Z"}')
        expected = singer.RecordMessage(
            record={'name': 'foo'},
            stream='users',
            version=2,
            time_extracted=dateutil.parser.parse("1970-01-02T00:00:00.000Z"))
        print(message)
        print(expected)
        self.assertEqual(message, expected)

    def test_extraction_time_strftime(self):
        """ Test that we're not corrupting timestamps with cross platform parsing. (Test case for OSX, specifically) """
        message = singer.RecordMessage(
            record={'name': 'foo'},
            stream='users',
            version=2,
            time_extracted=dateutil.parser.parse("1970-01-02T00:00:00.000Z"))
        expected = "1970-01-02T00:00:00.000000Z"
        self.assertEqual(message.asdict()["time_extracted"], expected)


    def test_parse_message_record_missing_record(self):
        with self.assertRaises(Exception):
            singer.parse_message('{"type": "RECORD", "stream": "users"}')

    def test_parse_message_record_missing_stream(self):
        with self.assertRaises(Exception):
            singer.parse_message(
                '{"type": "RECORD", "record": {"name": "foo"}}')

    def test_parse_message_schema_good(self):
        message = singer.parse_message('{"type": "SCHEMA", "stream": "users", "schema": {"type": "object", "properties": {"name": {"type": "string"}}}, "key_properties": ["name"]}')  # nopep8
        self.assertEqual(
            message,
            singer.SchemaMessage(
                stream='users',
                key_properties=['name'],
                schema={'type': 'object',
                        'properties': {
                            'name': {'type': 'string'}}}))

    def test_parse_message_schema_missing_stream(self):
        with self.assertRaises(Exception):
            message = singer.parse_message('{"type": "SCHEMA", "schema": {"type": "object", "properties": {"name": {"type": "string"}}}, "key_properties": ["name"]}')  # nopep8

    def test_parse_message_schema_missing_schema(self):
        with self.assertRaises(Exception):
            message = singer.parse_message(
                '{"type": "SCHEMA", "stream": "users", "key_properties": ["name"]}')  # nopep8

    def test_parse_message_schema_missing_key_properties(self):
        with self.assertRaises(Exception):
            message = singer.parse_message('{"type": "SCHEMA", "stream": "users", "schema": {"type": "object", "properties": {"name": {"type": "string"}}}}')  # nopep8

    def test_parse_message_state_good(self):
        message = singer.parse_message(
            '{"type": "STATE", "value": {"seq": 1}}')
        self.assertEqual(message, singer.StateMessage(value={'seq': 1}))

    def test_parse_message_state_missing_value(self):
        with self.assertRaises(Exception):
            singer.parse_message('{"type": "STATE"}')

    def test_round_trip(self):

        record_message = singer.RecordMessage(
            record={'name': 'foo'},
            stream='users')

        schema_message = singer.SchemaMessage(
            stream='users',
            key_properties=['name'],
            schema={'type': 'object',
                    'properties': {
                        'name': {'type': 'string'}}})

        state_message = singer.StateMessage(value={'seq': 1})
        
        self.assertEqual(record_message,
                         singer.parse_message(singer.format_message(record_message)))
        self.assertEqual(schema_message,
                         singer.parse_message(singer.format_message(schema_message)))
        self.assertEqual(state_message,
                         singer.parse_message(singer.format_message(state_message)))

    ## These three tests just confirm that writing doesn't throw

    def test_write_record(self):
        singer.write_record("users", {"name": "mike"})

    def test_write_schema(self):
        schema={'type': 'object',
                'properties': {
                    'name': {'type': 'string'}}}
        singer.write_schema("users", schema, ["name"])

    def test_write_state(self):
        singer.write_state({"foo": 1})

if __name__ == '__main__':
    unittest.main()
