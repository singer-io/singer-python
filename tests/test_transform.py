import unittest
from singer import transform
from singer.transform import *

class TestTransform(unittest.TestCase):
    def test_integer_transform(self):
        schema = {'type': 'integer'}
        self.assertEqual(123, transform(123, schema))
        self.assertEqual(123, transform('123', schema))
        self.assertEqual(1234, transform('1,234', schema))

    def test_nested_transform(self):
        schema =  {"type": "object",
                   "properties": {"addrs": {"type": "array",
                                            "items": {"type": "object",
                                                      "properties": {"addr1": {"type": "string"},
                                                                     "city": {"type": "string"},
                                                                     "state": {"type": "string"},
                                                                     'amount': {'type': 'integer'}}}}}}
        data = {'addrs': [{'amount': '123'}, {'amount': '456'}]}
        expected = {'addrs': [{'amount': 123}, {'amount': 456}]}
        self.assertEqual(expected, transform(data, schema))

    def test_null_transform(self):
        self.assertEqual('', transform('', {'type': ['null', 'string']}))
        self.assertEqual('', transform('', {'type': [ 'string', 'null']}))
        self.assertEqual(None, transform(None, {'type': [ 'string', 'null']}))
        self.assertEqual(None, transform('', {'type': ['null']}))
        self.assertEqual(None, transform(None, {'type': ['null']}))

    def test_datetime_transform(self):
        schema = {"type": "string", "format": "date-time"}
        string_datetime = "2017-01-01T00:00:00Z"
        self.assertEqual(string_datetime, transform(string_datetime, schema, NO_INTEGER_DATETIME_PARSING))
        self.assertEqual('1970-01-02T00:00:00Z', transform(86400, schema, UNIX_SECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual(string_datetime, transform(string_datetime, schema, UNIX_SECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual('1970-01-01T00:01:26Z', transform(86400, schema, UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual(string_datetime, transform(string_datetime, schema, UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING))

        with self.assertRaises(Exception):
            transform('cat', schema, NO_INTEGER_DATETIME_PARSING)
        with self.assertRaises(Exception):
            transform('cat', schema, UNIX_SECONDS_INTEGER_DATETIME_PARSING)
        with self.assertRaises(Exception):
            transform(0, schema, NO_INTEGER_DATETIME_PARSING)

    def test_error_path(self):
        schema = {"type": "object",
                  "properties": {"foo": {"type": "integer"},
                                 "baz": {"type": "integer"}}}
        data = {"foo": "bar", "baz": 1}
        # TODO: error_paths looks a little too nested
        self.assertEqual((False, None, [], [[['foo']]]), transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], []))

    def test_error_path(self):
        schema = {"type": "object",
                  "properties": {"key1": {"type": "object",
                                          "properties": {"key2": {"type": "object",
                                                                  "properties": {"key3": {"type": "object",
                                                                                          "properties": {"key4": {"type": "integer"}}}}}}}}}
        data = {"key1": {"key2": {"key3": {"key4": "not an integer"}}}}
        self.assertEqual((False, None, [], [[['key1', 'key2', 'key3', 'key4']]]),
                         transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], []))
