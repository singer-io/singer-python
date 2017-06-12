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

class TestHttpRequestTimer(unittest.TestCase):

    @patch('singer.metrics.log_metric')
    def test_success(self, log_metric):
        timer = metrics.http_request_timer('users')
        timer.elapsed = lambda: 0
        with timer:
            pass
        got = logged_metric(log_metric)
        self.assertEqual(
            [('timer', 'http_request_duration', 0, {'endpoint': 'users', 'status': 'succeeded'}),
             ('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'succeeded'})],
            got)

    @patch('singer.metrics.log_metric')
    def test_success_with_http_status_code(self, log_metric):
        with metrics.http_request_timer('users') as timer:
            timer.elapsed = lambda: 0
            timer.http_status_code = 200
        self.assertEqual(
            [('timer', 'http_request_duration', 0, {'endpoint': 'users', 'status': 'succeeded', 'http_status_code': 200}),
             ('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'succeeded', 'http_status_code': 200})],
            logged_metric(log_metric))

    @patch('singer.metrics.log_metric')
    def test_failure(self, log_metric):
        try:
            with metrics.http_request_timer('users') as timer:
                timer.elapsed = lambda: 0
                timer.http_status_code = 400
                raise ValueError('foo is not bar')
        except ValueError:
            pass
        self.assertEqual(
            [('timer', 'http_request_duration', 0, {'endpoint': 'users', 'status': 'failed', 'http_status_code': 400}),
             ('counter', 'http_request_count', 1, {'endpoint': 'users', 'status': 'failed', 'http_status_code': 400})],
            logged_metric(log_metric))        
