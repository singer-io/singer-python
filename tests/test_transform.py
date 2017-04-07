import unittest
from singer import transform


class TestTransform(unittest.TestCase):
    def test_integer_transform(self):
        schema = {'type': 'integer'}
        self.assertEqual(123, transform.transform(123, schema))
        self.assertEqual(123, transform.transform('123', schema))
        self.assertEqual(1234, transform.transform('1,234', schema))

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
        self.assertEqual(expected, transform.transform(data, schema))
        
    def test_null_transform(self):
        self.assertEqual('', transform.transform('', {'type': ['null', 'string']}))
        self.assertEqual('', transform.transform('', {'type': [ 'string', 'null']}))
        self.assertEqual(None, transform.transform(None, {'type': [ 'string', 'null']}))
        self.assertEqual(None, transform.transform('', {'type': ['null']}))
        self.assertEqual(None, transform.transform(None, {'type': ['null']}))
        
    def test_datetime_transform(self):
        schema = {"type": "string", "format": "date-time"}
        string_datetime = "2017-01-01T00:00:00Z"
        self.assertEqual(string_datetime, transform.transform(string_datetime, schema, transform.NO_INTEGER_DATETIME_PARSING))
        self.assertEqual('1970-01-02T00:00:00Z', transform.transform(86400, schema, transform.UNIX_SECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual(string_datetime, transform.transform(string_datetime, schema, transform.UNIX_SECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual('1970-01-01T00:01:26Z', transform.transform(86400, schema, transform.UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING))
        self.assertEqual(string_datetime, transform.transform(string_datetime, schema, transform.UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING))

        with self.assertRaises(Exception):
            transform.transform('cat', schema, transform.NO_INTEGER_DATETIME_PARSING)
        with self.assertRaises(Exception):
            transform.transform('cat', schema, transform.UNIX_SECONDS_INTEGER_DATETIME_PARSING)
        with self.assertRaises(Exception):
            transform.transform(0, schema, transform.NO_INTEGER_DATETIME_PARSING)
