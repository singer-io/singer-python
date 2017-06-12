import unittest
from unittest.mock import patch
import singer.metrics as metrics
import time
import copy

class DummyException(Exception):
    pass


def logged_metric(mock):
    return [args[1:] for args, _ in mock.call_args_list]


class TestRecordCounter(unittest.TestCase):

    @patch('singer.metrics.log_metric')
    def test_log_on_exit(self, log_metric):
        with metrics.record_counter('users') as counter:
            counter.increment()
            counter.increment()
        self.assertEqual(
            [('counter', 'record_count', 2, {'endpoint': 'users'})],
            logged_metric(log_metric))

    @patch('singer.metrics.log_metric')
    def test_incremental(self, log_metric):
        with metrics.record_counter(endpoint='users') as counter:
            counter.increment(1)
            counter._ready_to_log = lambda: True
            counter.increment(2)
            counter._ready_to_log = lambda: False
            counter.increment(5)
        self.assertEqual(
            [('counter', 'record_count', 3, {'endpoint': 'users'}),
             ('counter', 'record_count', 5, {'endpoint': 'users'})],             
            logged_metric(log_metric))

class TestHttpRequestCounter(unittest.TestCase):

    @patch('singer.metrics.log_metric')
    def test_success(self, log_metric):
        with metrics.http_request_counter('users') as counter:
            pass
        self.assertEqual(
            [('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'succeeded'})],
            logged_metric(log_metric))

    @patch('singer.metrics.log_metric')
    def test_success_with_http_status_code(self, log_metric):
        with metrics.http_request_counter('users') as counter:
            counter.http_status_code = 200
        self.assertEqual(
            [('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'succeeded', 'http_status_code': 200})],
            logged_metric(log_metric))

    @patch('singer.metrics.log_metric')
    def test_failure(self, log_metric):
        try:
            with metrics.http_request_counter('users') as counter:
                raise ValueError('foo is not bar')
        except ValueError:
            pass
        self.assertEqual(
            [('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'failed'})],
            logged_metric(log_metric))        

        
class TestTimer(unittest.TestCase):
    @patch('singer.metrics.log_metric')
    def test_success(self, log_metric):
        with metrics.http_request_timer('users'):
            pass
        got = logged_metric(log_metric)
        (_type, metric, value, tags) = logged_metric(log_metric)[0]
        self.assertEqual('timer', _type)
        self.assertEqual('http_request_duration', metric)
        self.assertEqual({'endpoint': 'users'}, tags)

