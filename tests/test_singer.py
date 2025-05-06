import singer
import unittest
from unittest.mock import patch
import datetime
import dateutil
from decimal import Decimal


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

class TestParsingNumbers(unittest.TestCase):
    def create_record(self, value):
        raw = '{"type": "RECORD", "stream": "test", "record": {"value": ' + value + '}}'
        parsed = singer.parse_message(raw)
        return parsed.record['value']

    def test_parse_int_zero(self):
        value = self.create_record('0')
        self.assertEqual(type(value), int)
        self.assertEqual(value, 0)

    def test_parse_regular_decimal(self):
        value = self.create_record('3.14')
        self.assertEqual(Decimal('3.14'), value)

    def test_parse_large_decimal(self):
        value = self.create_record('9999999999999999.9999')
        self.assertEqual(Decimal('9999999999999999.9999'), value)

    def test_parse_small_decimal(self):
        value = self.create_record('-9999999999999999.9999')
        self.assertEqual(Decimal('-9999999999999999.9999'), value)

    def test_parse_absurdly_large_decimal(self):
        value_str = '9' * 1024 + '.' + '9' * 1024
        value = self.create_record(value_str)
        self.assertEqual(Decimal(value_str), value)

    def test_parse_absurdly_large_int(self):
        value_str = '9' * 1024
        value = self.create_record(value_str)
        self.assertEqual(int(value_str), value)
        self.assertEqual(int, type(value))

    def test_parse_bulk_decs(self):
        value_strs = [
            '-9999999999999999.9999999999999999999999',
            '0',
            '9999999999999999.9999999999999999999999',
            '-7187498962233394.3739812942138415666763',
            '9273972760690975.2044306442955715221042',
            '29515565286974.1188802122612813004366',
            '9176089101347578.2596296292040288441238',
            '-8416853039392703.306423225471199148379',
            '1285266411314091.3002668125515694162268',
            '6051872750342125.3812886238958681227336',
            '-1132031605459408.5571559429308939781468',
            '-6387836755056303.0038029604189860431045',
            '4526059300505414'
        ]
        for value_str in value_strs:
            value = self.create_record(value_str)
            self.assertEqual(Decimal(value_str), value)

    @patch('sys.stdout')
    def test_ensure_ascii_false(self, mock_stdout):
        """
        Setting ensure_ascii=False will preserve special characters like é 
        in their original form.
        """
        rec = {"name": "José"}
        expected_output = '{"type": "RECORD", "stream": "test_stream", "record": {"name": "José"}}\n'
        rec_message = singer.RecordMessage(stream="test_stream", record=rec)
        result = singer.write_message(rec_message, ensure_ascii=False)
        mock_stdout.write.assert_called_once_with(expected_output)
        mock_stdout.flush.assert_called_once()

    @patch('sys.stdout')
    def test_ensure_ascii_true(self, mock_stdout):
        """
        ensure_ascii defaults to True, special characters like é are 
        escaped into their ASCII representation (e.g., \u00e9)
        """
        rec = {"name": "José"}
        expected_output = '{"type": "RECORD", "stream": "test_stream", "record": {"name": "Jos\\u00e9"}}\n'
        rec_message = singer.RecordMessage(stream="test_stream", record=rec)
        result = singer.write_message(rec_message)
        mock_stdout.write.assert_called_once_with(expected_output)
        mock_stdout.flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()
