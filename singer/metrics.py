'''Utilities for logging and parsing metrics.

A Tap should use this library to log structured messages about the read
operations it makes.
'''

import json
import json.decoder
import re
import time
import logging
import attr

DEFAULT_LOG_INTERVAL = 60

class Status:  # pylint: disable=too-few-public-methods
    '''Constants for status codes'''
    succeeded = 'succeeded'
    failed = 'failed'


class Metric:  # pylint: disable=too-few-public-methods
    '''Constants for metric names'''

    record_count = 'record_count'
    job_duration = 'job_duration'
    http_request_duration = 'http_request_duration'


class Tag:  # pylint: disable=too-few-public-methods
    '''Constants for commonly used tags'''
    endpoint = 'endpoint'
    http_status_code = 'http_status_code'
    status = 'status'

@attr.s
class DataPoint:
    metric_type = attr.ib()
    metric = attr.ib()
    value = attr.ib()
    tags = attr.ib(default=attr.Factory(dict))


def log(logger, data_point):
    '''Log a single data point.'''
    result = {
        'type': data_point.metric_type,
        'metric': data_point.metric,
        'value': data_point.value,
        'tags': data_point.tags
    }
    logger.info('METRIC: %s', json.dumps(result))



class Counter(object):  # pylint: disable=too-few-public-methods
    '''Increments a counter metric.

    When you use Counter as a context manager, it will automatically emit
    "counter" metrics periodically and also when the context exits. The
    only thing you need to do is initialize the Counter and then call
    increment().

    >>> with singer.metrics.Counter(metric='record_count', endpoint='users') as counter:
    >>>    for user in get_users(...):
    >>>        # Print out the user
    >>>        counter.increment()

    This would print a metric like this:

    {
      "type":   "counter",
      "metric": "record_count",
      "value":   12345,
      "tags": {
        "endpoint": "users",
      }
    }

    '''

    def __init__(self, metric, endpoint=None, log_interval=DEFAULT_LOG_INTERVAL):
        self.metric = metric
        self.endpoint = endpoint
        self.log_interval = log_interval

        self.value = 0
        self.logger = logging.getLogger(__name__)
        self.last_log_time = None

    def __enter__(self):
        self.last_log_time = time.time()
        return self

    def increment(self, amount=1):
        '''Increments value by the specified amount.'''
        self.value += amount
        if self._ready_to_log():
            self._pop()

    def _pop(self):
        value = self.value
        self.value = 0
        self.last_log_time = time.time()
        data_point = DataPoint('counter', self.metric, value)
        data_point.tags[Tag.endpoint] = self.endpoint
        log(self.logger, data_point)

    def __exit__(self, exc_type, exc_value, traceback):
        self._pop()

    def _ready_to_log(self):
        return time.time() - self.last_log_time > self.log_interval


class Timer(object):  # pylint: disable=too-few-public-methods
    '''Produces metrics about the duration of operations.

    You use a Timer as a context manager wrapping around some operation.
    When the context exits, the Timer emits a metric that indicates how
    long (in seconds) the operation took.

    It will automatically include a "status" tag that is "failed" if the
    context exits with an Exception or "success" if it exits cleanly. You
    can override this by setting timer.status within the context.

    >>> with singer.metrics.Timer(duration_metric="request_duration",
    >>>                           counter_metric="request_count",
    >>>                           endpoint="users"):
    >>>    # Do some stuff

    This produces a metric like this:

    {
      "type": "timer",
      "metric": "request_duration",
      "value": 1.23,
      "tags": {
        "endpoint": "users",
        "status": "success"
      }
    },

    '''
    def __init__(self, metric, endpoint):
        self.metric = metric
        self.endpoint = endpoint
        self.http_status_code = None
        self.status = None
        self.logger = logging.getLogger(__name__)
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def elapsed(self):
        '''Return elapsed time'''
        return time.time() - self.start_time

    def __exit__(self, exc_type, exc_value, traceback):
        data_point = DataPoint('timer', self.metric, self.elapsed())

        for k in [Tag.endpoint,
                  Tag.http_status_code,
                  Tag.status]:
            if self.__dict__[k] is not None:
                data_point.tags[k] = self.__dict__[k]

        print('The data point is ' + str(data_point))
        if Tag.status not in data_point.tags:
            if exc_type is None:
                data_point.tags[Tag.status] = Status.succeeded
            else:
                data_point.tags[Tag.status] = Status.failed
        log(self.logger, data_point)


def record_counter(endpoint=None, log_interval=DEFAULT_LOG_INTERVAL):
    '''Use for counting records retrieved from the source.

    >>> with singer.metrics.record_counter("users") as counter:
    >>>     for user in some_source_of_users():
    >>>         # Do something with the user
    >>>         counter.increment()
    '''
    return Counter(Metric.record_count, endpoint, log_interval=log_interval)


def http_request_timer(endpoint):
    '''Use for timing and counting HTTP requests to an endpoint

    >>> with singer.metrics.http_request_timer("users") as timer:
    >>>     # Make a request
    '''
    return Timer(Metric.http_request_duration, endpoint)


def parse(line):
    '''Parse a DataPoint from a log line and return it, or None if no data point.'''
    match = re.match(r'^INFO METRIC: (.*)$', line)
    if match:
        json_str = match.group(1)
        try:
            raw = json.loads(json_str)
            return DataPoint(
                metric_type=raw.get('type'),
                metric=raw.get('metric'),
                value=raw.get('value'),
                tags=raw.get('tags'))
        except Exception as exc:  # pylint: disable=broad-except
            logging.getLogger(__name__).warning('Error parsing metric: %s', exc)
    return None
