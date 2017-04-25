'''Utilities for logging and parsing stats.

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

If you use the singer.stats.Timer() context manager, you'll automatically
get status and duration. Status is 'running' while we're in the context
manager, 'succeeded' after we exit the context manager if no exception was
raised, and 'failed' if an exception was raised. Duration is the time in
seconds that the thread spent inside the context manager.

    >>> with singer.stats.Stats() as stats:
    >>>    # Do some stuff

This will log a message like:

    {"duration": 1.23,
     "status": "succeeded"}

You can also include a record count and the HTTP status code (when
applicable) simply by setting properties on the stats object.

    >>> with singer.stats.Timer(source='orders') as stats:
    >>>     resp = requests.get('http://myapi.com/orders')
    >>>     stats.http_status_code = resp.status_code
    >>>     resp.raise_for_status()
    >>>     stats.record_count = len(resp.json()['orders'])

This will log a message like:

    {"source": "orders",
     "duration": 1.23,
     "succeeded": true,
     "record_count": 234,
     "http_status_code": 200}

If your Tap gets records continuously rather than in discrete batches, you
can use a singer.stats.Counter to periodically emit stats messages.

    >>> with singer.stats.Counter(source='orders', interval=30) as stats:
    >>>     for order in some_client.orders():
    >>>         stats.add(record_count=1)

This would print a message about every 30 seconds indicating the current
status and how many records have been fetched since the last message was
logged.

    {"source": "orders", "record_count": 1234, "status": "running"}
    {"source": "orders", "record_count": 1111, "status": "running"}
    {"source": "orders", "record_count": 1212, "status": "succeeded"}

It is recommended to use a short name for the source (such as "orders")
rather than a full URL, so that an application consuming the logs can
easily group together stats related to requests to the same logical
source.

'''

import json
import json.decoder
import re
import time
import logging


class Field:  # pylint: disable=too-few-public-methods
    '''Field names for stats messages'''

    # Metrics
    record_count = 'record_count'
    byte_count = 'byte_count'
    duration = 'duration'

    # Tags
    source = 'source'
    status = 'status'
    http_status_code = 'http_status_code'

class Status:  # pylint: disable=too-few-public-methods
    succeeded = 'succeeded'
    running = 'running'
    failed = 'failed'

FIELDS = [
    Field.record_count,
    Field.byte_count,
    Field.duration,

    Field.source,
    Field.status,
    Field.http_status_code
]

def log_stats(logger, stats):
    logger.info('STATS: %s', json.dumps(stats))

def prune_and_log_stats(logger, stats):
    log_stats(logger, {k: v for k, v in stats.items() if v is not None})

class Counter(object):  # pylint: disable=too-few-public-methods

    def __init__(self, source=None, log_interval=60):
        self.logger = logging.getLogger(__name__)
        self.source = source
        self.record_count = None
        self.byte_count = None
        self.last_log_time = None
        self.log_interval = log_interval
        self.status = None

    def __enter__(self):
        self.last_log_time = time.time()
        self.status = Status.running
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.status = Status.succeeded if exc_type is None else Status.failed
        prune_and_log_stats(self.logger, self._pop_stats())

    def _pop_stats(self):
        result = {
            'source': self.source,
            'status': self.status,
            'record_count': self.record_count,
            'byte_count': self.byte_count
        }
        self.record_count = None
        self.byte_count = None
        self.last_log_time = time.time()
        return result

    def add(self, record_count=None, byte_count=None):
        '''Increments record_count and byte_count by the specified amounts.

        Only increments each field if the provided value is not None.

        '''
        if record_count:
            if not self.record_count:
                self.record_count = 0
            self.record_count += record_count
        if byte_count:
            if not self.byte_count:
                self.byte_count = 0
            self.byte_count += 0

        if self._ready_to_log():
            prune_and_log_stats(self.logger, self._pop_stats())

    def _ready_to_log(self):
        return time.time() - self.last_log_time > self.log_interval


class Timer(object):  # pylint: disable=too-few-public-methods
    '''Captures timing stats and logs them.'''

    def __init__(self, source=None):
        self.logger = logging.getLogger(__name__)
        self.source = source
        self.record_count = None
        self.byte_count = None
        self.http_status_code = None
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        stats = {
            'duration': time.time() - self.start_time,
            'status': Status.succeeded if exc_type is None else Status.failed,
            'http_status_code': self.http_status_code,
            'source': self.source,
            'record_count': self.record_count,
            'byte_count': self.byte_count
        }
        prune_and_log_stats(self.logger, stats)


def parse_stats(line):
    '''Parse stats from a log line and return them as a dict.'''
    match = re.match(r'^INFO STATS: (.*)$', line)
    result = None
    if match:
        json_str = match.group(1)
        try:
            result = json.loads(json_str)
        except Exception as exc:  # pylint: disable=broad-except
            logging.getLogger(__name__).warning('Error parsing stats: %s', exc)
    return result
