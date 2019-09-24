import unittest
from datetime import datetime as dt
import pytz
import logging
import json
import tempfile
import singer.utils as u


class TestFormat(unittest.TestCase):
    def test_small_years(self):
        self.assertEqual(u.strftime(dt(90, 1, 1, tzinfo=pytz.UTC)),
                         "0090-01-01T00:00:00.000000Z")

    def test_round_trip(self):
        now = dt.utcnow().replace(tzinfo=pytz.UTC)
        dtime = u.strftime(now)
        pdtime = u.strptime_to_utc(dtime)
        fdtime = u.strftime(pdtime)
        self.assertEqual(dtime, fdtime)


class TestHandleException(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)

    def test_successful_fn(self):
        @u.handle_top_exception(self.logger)
        def foo():
            return 3
        self.assertEqual(foo(), 3)

    def test_exception_fn(self):
        @u.handle_top_exception(self.logger)
        def foo():
            raise RuntimeError("foo")
        self.assertRaises(RuntimeError, foo)

class TestLoadJson(unittest.TestCase):
    def setUp(self):
        self.expected_json = """
            {
                "key1": false,
                "key2": [
                    {"field1": 366, "field2": "2018-01-01T00:00:00+00:00"}
                ]
            }
        """

    def test_inline(self):
        inline = u.load_json(self.expected_json)
        self.assertEqual(inline, json.loads(self.expected_json))

    def test_path(self):
        # from valid path
        with tempfile.NamedTemporaryFile() as fil:
            fil.write(self.expected_json.encode())
            fil.seek(0)
            from_path = u.load_json(fil.name)
            self.assertEqual(from_path, json.loads(self.expected_json))
        # from invalid path
        self.assertRaises(FileNotFoundError, u.load_json, 'does_not_exist.json')
