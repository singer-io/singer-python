import unittest
from datetime import datetime as dt
from datetime import timezone as tz
import singer.utils as u


class TestFormat(unittest.TestCase):
    def test_small_years(self):
        self.assertEqual(u.strftime(dt(90, 1, 1, tzinfo=tz.utc)),
                         "0090-01-01T00:00:00.000000Z")
