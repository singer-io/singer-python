'''Utilities for logging and parsing stats.

A Tap should use this library to log a structured message about each fetch
operation it makes. The message is a flat map, with a small key set,
designed to be easy to convert to a metric for some popular monitoring
tools (AWS CloudWatch, Datadog).

    record_count      Number of records fetched in this operation
    byte_count        Number of bytes fetched in this operation
    duration          Duration of the operation in seconds
    source            Source of the data, as a string
    succeeded         True if the operation succeeded, False otherwise
    http_status_code  The HTTP status code of the response

All fields are considered optional. A Tap should only include fields that
are relevant to the operation and that it can reliably compute.

If you use the singer.stats.Stats() context manager, you'll automatically
get succeeded and duration. Succeeded is False if an Exception was raised,
True otherwise. Duration is the time in seconds that the thread spent
inside the context manager.

    >>> with singer.stats.Stats() as stats:
    >>>    # Do some stuff

This will log a message like:

    {"duration": 1.23,
     "succeeded": true}

A Tap that pulls records from a database could additionally include record
count:

    >>> with singer.stats.Stats() as stats:
    >>>     cursor = conn.execute('SELECT * FROM orders')
    >>>     stats.record_count = cursor.rowcount
    >>>     for order in cursor:
    >>>         singer.write_record('orders', order)

This will log a message like:

    {"duration": 1.23,
     "succeeded": true,
     "record_count": 234}

A Tap that makes HTTP requests could additionally include a logical name
for the endpoint and the http_status_code:

    >>> with singer.stats.Stats(source='orders') as stats:
    >>>     resp = requests.get('http://myapi.com/orders')
    >>>     stats.http_status_code = resp.status_code
    >>>     resp.raise_for_status()
    >>>     stats.record_count = len(resp.json()['orders'])

This will log a message like:

    {"duration": 1.23,
     "succeeded": true,
     "record_count": 234,
     "http_status_code": 200}

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
    succeeded = 'succeeded'
    http_status_code = 'http_status_code'


FIELDS = [
    Field.record_count,
    Field.byte_count,
    Field.duration,
    Field.source,
    Field.succeeded,
    Field.http_status_code
]


def _cleanup_stats(stats):
    return {k: v for k, v in stats.items() if v is not None}


def log_stats(stats):
    '''Log a stats message at INFO level.

    stats should be a dict with the field set restricted to the fields
    in singer.stats.Fields.

    '''
    logging.getLogger(__name__).info('STATS: %s', json.dumps(_cleanup_stats(stats)))


class Stats(object):  # pylint: disable=too-few-public-methods
    '''Captures timing stats and logs them.'''

    def __init__(self, source=None):
        self.source = source
        self.record_count = None
        self.byte_count = None
        self.http_status_code = None
        self.start_time = None
        self.result = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.time() - self.start_time
        succeeded = exc_type is None
        self.result = {
            'record_count': self.record_count,
            'byte_count': self.byte_count,
            'duration': duration,
            'source': self.source,
            'succeeded': succeeded,
            'http_status_code': self.http_status_code
        }
        log_stats(self.result)

    def increment_record_count(self):
        '''None-safe method to increment record_count.'''

        if not self.record_count:
            self.record_count = 0
        self.record_count += 1


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
