import json
import logging
import os
import re
import time

import attr
import singer


def init_logger():
    this_dir, _ = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)


class Field:
    # Metrics
    fetch_count = 'fetch_count'
    record_count = 'record_count'
    byte_count = 'byte_count'
    duration = 'duration'

    # Tags
    source = 'source'
    succeeded = 'succeeded'
    http_status = 'http_status'


def log_fetch_stats(fetch_count=None,
                    record_count=None,
                    byte_count=None,
                    duration=None,
                    source=None,
                    succeeded=None,
                    http_status=None):

    stats = {}
    if fetch_count: stats[Field.fetch_count] = fetch_count
    if record_count: stats[Field.record_count] = record_count
    if byte_count: stats[Field.byte_count] = byte_count 
    if duration: stats[Field.duration] = duration
    
    if source: stats[Field.source] = source
    if succeeded: stats[Field.succeeded] = succeeded
    if http_status: stats[Field.http_status] = http_status

    logging.getLogger('root').info('FETCH_STATS: %s', json.dumps(stats))        

@attr.s()
class FetchStats(object):
    source = attr.ib()
    record_count = attr.ib(default=None)
    byte_count = attr.ib(default=None)
    
    http_status = attr.ib(default=None)

    start_time = attr.ib(default=None)
    
    def __enter__(self):
        self.start_time = time.time()
        init_logger()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.time() - self.start_time
        succeeded = exc_type is None

        log_fetch_stats(fetch_count=1,
                        record_count=self.record_count,
                        byte_count=self.byte_count,
                        duration=duration,
                        source=self.source,
                        succeeded=succeeded,
                        http_status=self.http_status)

    def increment_record_count(self):
        if not self.record_count:
            self.record_count = 0
        self.record_count += 1

        
def parse_fetch_stats(line):
    match = re.match(r'FETCH_STATS: {\.*}')
    json_str = match.groups(1)
    parsed = json.loads(json_str)
    return parsed


if __name__ == '__main__':

    with FetchStats(source='users') as stats:
        for i in range(20):
            stats.increment_record_count()
        time.sleep(1.5)
