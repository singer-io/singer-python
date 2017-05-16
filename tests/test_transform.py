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

    def test_anyof_datetime(self):
        schema = {'anyOf': [{'type': 'null'}, {'format': 'date-time', 'type': 'string'}]}
        string_datetime = '2016-03-10T18:47:20Z'
        self.assertEqual(string_datetime, transform(string_datetime, schema))
        self.assertEqual(None, transform(None, schema))

    def test_error_path(self):
        schema = {"type": "object",
                  "properties": {"foo": {"type": "integer"},
                                 "baz": {"type": "integer"}}}
        data = {"foo": "bar", "baz": 1}
        self.assertEqual((False, None, [], [['foo']]), transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], []))

    def test_nested_error_path_throws(self):
        schema = {"type": "object",
                  "properties": {"key1": {"type": "object",
                                          "properties": {"key2": {"type": "object",
                                                                  "properties": {"key3": {"type": "object",
                                                                                          "properties": {"key4": {"type": "integer"}}}}}}}}}
        data = {"key1": {"key2": {"key3": {"key4": "not an integer"}}}}
        self.assertEqual((False, None, [], [['key1', 'key2', 'key3', 'key4']]),
                         transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], []))

    def test_nested_error_path_no_throw(self):
        schema = {"type": "object",
                  "properties": {"key1": {"type": "object",
                                          "properties": {"key2": {"type": "object",
                                                                  "properties": {"key3": {"type": "object",
                                                                                          "properties": {"key4": {"type": "string"},
                                                                                                         "key5": {"type": "string"}}}}}}}}}
        data = {"key1": {"key2": {"key3": {"key4": None, "key5": None}}}}
        success, data, _, error_paths = transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], [])
        self.assertEqual(False, success)
        self.assertEqual(None, data)
        # NB> error_paths may be returned in any order, so we sort here to be deterministic
        self.assertEqual(sorted(error_paths), sorted([['key1', 'key2', 'key3', 'key4'], ['key1', 'key2', 'key3', 'key5']]))

    def test_error_path_array(self):
        schema =  {"type": "object",
                   "properties": {"integers": {"type": "array",
                                               "items": {"type": "integer"}}}}
        data = {"integers": [1, 2, "not an integer", 4, "also not an integer"]}
        success, _, _, error_paths = transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], [])
        self.assertEqual(False, success)
        # NB> error_paths may be returned in any order, so we sort here to be deterministic
        self.assertEqual(sorted(error_paths), sorted([["integers", 2], ["integers", 4]]))

    def test_nested_error_path_array(self):
        schema =  {"type": "object",
                   "properties": {"lists_of_integers": {"type": "array",
                                                        "items": {"type": "array",
                                                                  "items": {"type": "integer"}}}}}
        data = {"lists_of_integers": [[1, "not an integer"], [2, 3], ["also not an integer", 4]]}
        success, _, _, error_paths = transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], [])
        self.assertEqual(False, success)
        # NB> error_paths may be returned in any order, so we sort here to be deterministic
        self.assertEqual(sorted(error_paths), sorted([["lists_of_integers", 0, 1], ["lists_of_integers", 2, 0]]))

    def test_error_path_datetime(self):
        schema = {"type": "object",
                  "properties": {"good_datetime": {"type": "string", "format": "date-time"},
                                 "bad_datetime1": {"type": "string", "format": "date-time"},
                                 "bad_datetime2": {"type": "string", "format": "date-time"}}}
        data = {"good_datetime": "2017-04-11T16:07:00Z",
                "bad_datetime1": "not a datetime",
                "bad_datetime2": 1}
        success, _, _, error_paths = transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], [])
        self.assertEqual(False, success)
        self.assertEqual(sorted(error_paths), sorted([['bad_datetime1'], ['bad_datetime2']]))

    def test_unexpected_object_properties(self):
        schema = {"type": "object",
                  "properties": {"good_property": {"type": "string"}}}
        data = {"good_property": "expected data",
                "bad_property": "unexpected data"}
        success, transformed_data, _, _ = transform_recur(data, schema, NO_INTEGER_DATETIME_PARSING, [], [])
        self.assertEqual(True, success)
        self.assertEqual({"good_property": "expected data"}, transformed_data)
