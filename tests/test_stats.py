import unittest
from unittest.mock import patch
import singer.stats
import time
import copy

class DummyException(Exception):
    pass


def logged_stats(mock):
    return [args[1] for args, _ in mock.call_args_list]


class TestStats(unittest.TestCase):

    @patch('singer.stats.log_stats')
    def test_success_exit_only(self, log_stats):
        with singer.stats.Counter(source='foo') as stats:
            stats.add(record_count=1)
            stats.add(record_count=2)
        self.assertEqual(
            [{'source': 'foo', 'record_count': 3, 'status': 'succeeded'}],
            logged_stats(log_stats))

    @patch('singer.stats.log_stats')        
    def test_incremental(self, log_stats):
        with singer.stats.Counter(source='foo') as stats:
            stats.add(record_count=1)
            stats._ready_to_log = lambda: True
            stats.add(record_count=2)
            stats._ready_to_log = lambda: False
            stats.add(record_count=5)
        self.assertEqual(
            [{'source': 'foo', 'record_count': 3, 'status': 'running'},
             {'source': 'foo', 'record_count': 5, 'status': 'succeeded'}],
            logged_stats(log_stats))

    @patch('singer.stats.log_stats')        
    def test_failure(self, log_stats):
        try:
            with singer.stats.Counter(source='foo') as stats:
                stats.add(record_count=2)
                raise DummyException()
                stats.add(record_count=1)
        except DummyException:
            pass

        self.assertEqual(
            [{'source': 'foo', 'record_count': 2, 'status': 'failed'}],
            logged_stats(log_stats))


class TestTimer(unittest.TestCase):
    @patch('singer.stats.log_stats')
    def test_success(self, log_stats):
        with singer.stats.Timer(source='foo') as stats:
            stats.record_count = 3
        got = logged_stats(log_stats)
        self.assertEqual('foo', got[0]['source'])
        self.assertEqual('succeeded', got[0]['status'])
        self.assertEqual(3, got[0]['record_count'])
        self.assertTrue(isinstance(got[0]['duration'], float))

    @patch('singer.stats.log_stats')        
    def test_failure(self, log_stats):
        try:
            with singer.stats.Timer(source='foo') as stats:
                stats.record_count = 2
                raise DummyException()
        except DummyException:
            pass

        got = logged_stats(log_stats)
        self.assertEqual('foo', got[0]['source'])
        self.assertEqual('failed', got[0]['status'])
        self.assertEqual(2, got[0]['record_count'])
        self.assertTrue(isinstance(got[0]['duration'], float))

class TestParseStats(unittest.TestCase):
    
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
