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

    def test_parse_stats_success(self):
        line = 'INFO STATS: {"record_count": 100, "duration": 1, "http_status_code": 200, "source": "addresses", "succeeded": true}'
        expected = {
            'record_count': 100,
            'duration': 1,
            'http_status_code': 200,
            'source': 'addresses',
            'succeeded': True
        }
        self.assertEqual(expected, singer.stats.parse_stats(line))

    def test_parse_stats_fail_not_json(self):
        line = 'INFO STATS: something not json'
        self.assertIsNone(singer.stats.parse_stats(line))

    def test_parse_stats_fail_no_match(self):
        line = 'some other line'
        self.assertIsNone(singer.stats.parse_stats(line))
