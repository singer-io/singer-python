'''Utilities for logging stats'''

import json
import re
import time
import logging

LOGGER = logging.getLogger(__name__)

class Field: # pylint: disable=too-few-public-methods
    '''Field names for stats messages'''

    # Metrics
    fetch_count = 'fetch_count'
    record_count = 'record_count'
    byte_count = 'byte_count'
    duration = 'duration'

    # Tags
    source = 'source'
    succeeded = 'succeeded'
    http_status = 'http_status'


FIELDS = [
    Field.fetch_count,
    Field.record_count,
    Field.byte_count,
    Field.duration,
    Field.source,
    Field.succeeded,
    Field.http_status
]


def _cleanup_stats(stats):
    return {k: v for k, v in stats.items() if v is not None}


def log_stats(stats):
    '''Log a stats message at INFO level.

    stats should be a dict with the field set restricted to the fields
    in singer.stats.Fields.

    '''
    logging.getLogger('root').info('STATS: %s', json.dumps(_cleanup_stats(stats)))


class Stats(object): # pylint: disable=too-few-public-methods
    '''Captures timing stats and logs them.'''

    def __init__(self, source=None):
        self.source = source
        self.record_count = None
        self.byte_count = None
        self.http_status = None
        self.start_time = None


    def __enter__(self):
        self.start_time = time.time()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.time() - self.start_time
        succeeded = exc_type is None
        stats = {
            'fetch_count': 1,
            'record_count': self.record_count,
            'byte_count': self.byte_count,
            'duration': duration,
            'source': self.source,
            'succeeded': succeeded,
            'http_status': self.http_status
        }
        log_stats(stats)


    def increment_record_count(self):
        '''None-safe method to increment record_count.'''

        if not self.record_count:
            self.record_count = 0
        self.record_count += 1


def parse_stats(line):
    '''Parse stats from a log line and return them as a dict.'''
    match = re.match(r'STATS: {\.*}', line)
    json_str = match.groups(1)
    parsed = json.loads(json_str)
    return parsed
