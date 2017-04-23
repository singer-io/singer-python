import unittest
import singer.stats
import time


class DummyException(Exception):
    pass

class TestStats(unittest.TestCase):

    def test_with_stats_success(self):
        with singer.stats.Stats(source='foo') as stats:
            time.sleep(0.01)
            stats.increment_record_count()
            stats.increment_record_count()
        self.assertEqual('foo', stats.result['source'])
        self.assertTrue(stats.result['succeeded'])
        self.assertEqual(2, stats.result['record_count'])

    def test_with_stats_failure(self):
        try:
            with singer.stats.Stats(source='foo') as stats:
                time.sleep(0.01)
                stats.increment_record_count()
                stats.increment_record_count()
                raise DummyException()
                stats.increment_record_count()
        except DummyException:
            pass

        self.assertEqual('foo', stats.result['source'])
        self.assertFalse(stats.result['succeeded'])
        self.assertEqual(2, stats.result['record_count'])
