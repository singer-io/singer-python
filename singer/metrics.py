'''Utilities for logging and parsing metrics.

A Tap should use this library to log a structured message about each read
operation it makes. The message is a flat map, with a small key set,
designed to be easy to convert to a metric for some popular monitoring
tools (AWS CloudWatch, Datadog).

    record_count      Number of records fetched in this operation
    byte_count        Number of bytes fetched in this operation
    duration          Duration of the operation in seconds
    source            Source of the data, as a string
    status            Either 'running', 'succeeded', or 'failed'
    http_status_code  The HTTP status code of the response

All fields are considered optional. A Tap should only include fields that
are relevant to the operation and that it can reliably compute.

If you use the singer.metrics.Timer() context manager, you'll automatically
get status and duration. Status is 'running' while we're in the context
manager, 'succeeded' after we exit the context manager if no exception was
raised, and 'failed' if an exception was raised. Duration is the time in
seconds that the thread spent inside the context manager.

    >>> with singer.metrics.Timer() as timer:
    >>>    # Do some stuff

This will log a message like:

    {"duration": 1.23,
     "status": "succeeded"}

You can also include a record count and the HTTP status code (when
applicable) simply by setting properties on the metrics object.

    >>> with singer.metrics.Timer(source='orders') as timer:
    >>>     resp = requests.get('http://myapi.com/orders')
    >>>     timer.http_status_code = resp.status_code
    >>>     resp.raise_for_status()
    >>>     timer.record_count = len(resp.json()['orders'])

This will log a message like:

    {"duration": 1.23,
     "record_count": 234,
     "source": "orders",
     "status": "succeeded",
     "http_status_code": 200}

If your Tap gets records continuously rather than in discrete batches, you
can use a singer.metrics.Counter to periodically emit metrics messages.

    >>> with singer.metrics.Counter(source='orders', interval=30) as counter:
    >>>     for order in some_client.orders():
    >>>         counter.add(record_count=1)

This would print a message about every 30 seconds indicating the current
status and how many records have been fetched since the last message was
logged.

    {
        "metrics": {
            "record_count": 1234
        },
        "tags": {
            "status": "running"
        }
    }
    {
        "metrics": {
            "record_count": 1111
        },
        "tags": {
            "status": "running"
        }
    }
    {
        "metrics": {
            "record_count": 1212
        },
        "tags": {
            "status": "succeeded"
        }
    }

It is recommended to use a short name for the source (such as "orders")
rather than a full URL, so that an application consuming the logs can
easily group together metrics related to requests to the same logical
source.

'''

import json
import json.decoder
import re
import time
import logging


class Status:  # pylint: disable=too-few-public-methods
    '''Constants for status codes'''
    succeeded = 'succeeded'
    running = 'running'
    failed = 'failed'

class Metric:  # pylint: disable=too-few-public-methods
    '''Constants for metric names'''
    record_count = 'record_count'
    byte_count = 'byte_count'
    duration = 'duration'
    http_request_duration = 'http_request_duration'
    http_request_count = 'http_request_count'

class Tag:  # pylint: disable=too-few-public-methods
    '''Constants for commonly used tags'''
    endpoint = 'endpoint'
    http_status_code = 'http_status_code'
    status = 'status'


def log_metric(logger, metric_type, metric, value, tags):
    result = {
        'type': metric_type,
        'metric': metric,
        'value': value,
        'tags': tags
    }
    logger.info('METRIC: %s', json.dumps(result))


DEFAULT_LOG_INTERVAL = 60


class ItemCounter(object):  # pylint: disable=too-few-public-methods

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
            self._pop_metric()

    def _pop_metric(self):
        value = self.value
        self.value = 0
        self.last_log_time = time.time()
        log_metric(self.logger, 'counter', self.metric, value, {Tag.endpoint: self.endpoint})

    def __exit__(self, exc_type, exc_value, traceback):
        self._pop_metric()

    def _ready_to_log(self):
        return time.time() - self.last_log_time > self.log_interval


class OperationCounter(object):  # pylint: disable=too-few-public-methods

    def __init__(self, metric, endpoint=None):
        self.metric = metric
        self.endpoint = endpoint
        self.http_status_code = None
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        tags = {}
        if self.endpoint:
            tags[Tag.endpoint] = self.endpoint
        if exc_type is None:
            tags[Tag.status] = Status.succeeded
        else:
            tags[Tag.status] = Status.failed
        if self.http_status_code:
            tags[Tag.http_status_code] = self.http_status_code
        log_metric(self.logger, 'counter', self.metric, 1, tags)


class Timer(object):  # pylint: disable=too-few-public-methods
    '''Captures timing metrics and logs them.'''

    def __init__(self, metric, endpoint):
        self.metric = metric
        self.endpoint = endpoint
        self.logger = logging.getLogger(__name__)
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.time() - self.start_time,
        tags = {}
        if self.endpoint:
            tags[Tag.endpoint] = self.endpoint
        log_metric(self.logger, 'timer', self.metric, duration, tags)


def record_counter(endpoint=None, log_interval=DEFAULT_LOG_INTERVAL):
    '''Returns an ItemCounter for counting records retrieved from the source'''
    return ItemCounter(Metric.record_count, endpoint, log_interval=log_interval)


def http_request_timer(endpoint):
    '''Use for timing HTTP requests to an endpoint'''
    return Timer(Metric.http_request_duration, endpoint)


def http_request_counter(endpoint):
    '''Use for counting HTTP requests to an endpoint'''
    return OperationCounter(Metric.http_request_count, endpoint)


def parse_metrics(line):
    '''Parse metrics from a log line and return them as a dict.'''
    match = re.match(r'^INFO METRIC: (.*)$', line)
    result = None
    if match:
        json_str = match.group(1)
        try:
            result = json.loads(json_str)
        except Exception as exc:  # pylint: disable=broad-except
            logging.getLogger(__name__).warning('Error parsing metric: %s', exc)
    return result

