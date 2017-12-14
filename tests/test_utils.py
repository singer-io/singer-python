import unittest
from datetime import datetime as dt
from datetime import timezone as tz
import logging
import singer.utils as u


class TestFormat(unittest.TestCase):
    def test_small_years(self):
        self.assertEqual(u.strftime(dt(90, 1, 1, tzinfo=tz.utc)),
                         "0090-01-01T00:00:00.000000Z")


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
