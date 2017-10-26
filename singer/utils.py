import argparse
import collections
import datetime
import functools
import json
import time
import dateutil
import pytz
import backoff as backoff_module

from singer.catalog import Catalog

DATETIME_PARSE = "%Y-%m-%dT%H:%M:%SZ"
DATETIME_FMT = "%04Y-%m-%dT%H:%M:%S.%fZ"

def now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

def strptime_with_tz(dtime):
    d_object = dateutil.parser.parse(dtime)
    if d_object.tzinfo is None:
        return d_object.replace(tzinfo=pytz.UTC)

    return d_object

def strptime(dtime):
    try:
        return datetime.datetime.strptime(dtime, DATETIME_FMT)
    except Exception:
        return datetime.datetime.strptime(dtime, DATETIME_PARSE)

def strftime(dtime):
    if dtime.utcoffset() != datetime.timedelta(0):
        raise Exception("datetime must be pegged at UTC tzoneinfo")
    return dtime.strftime(DATETIME_FMT)

def ratelimit(limit, every):
    def limitdecorator(func):
        times = collections.deque()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(times) >= limit:
                tim0 = times.pop()
                tim = time.time()
                sleep_time = every - (tim - tim0)
                if sleep_time > 0:
                    time.sleep(sleep_time)

            times.appendleft(time.time())
            return func(*args, **kwargs)

        return wrapper

    return limitdecorator


def chunk(array, num):
    for i in range(0, len(array), num):
        yield array[i:i + num]


def load_json(path):
    with open(path) as fil:
        return json.load(fil)


def update_state(state, entity, dtime):
    if dtime is None:
        return

    if isinstance(dtime, datetime.datetime):
        dtime = strftime(dtime)

    if entity not in state:
        state[entity] = dtime

    if dtime >= state[entity]:
        state[entity] = dtime


def parse_args(required_config_keys):
    '''Parse standard command-line args.

    Parses the command-line arguments mentioned in the SPEC and the
    BEST_PRACTICES documents:

    -c,--config     Config file
    -s,--state      State file
    -d,--discover   Run in discover mode
    -p,--properties Properties file: DEPRECATED, please use --catalog instead
    --catalog       Catalog file

    Returns the parsed args object from argparse. For each argument that
    point to JSON files (config, state, properties), we will automatically
    load and parse the JSON file.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        required=True)

    parser.add_argument(
        '-s', '--state',
        help='State file')

    parser.add_argument(
        '-p', '--properties',
        help='Property selections: DEPRECATED, Please use --catalog instead')

    parser.add_argument(
        '--catalog',
        help='Catalog file')

    parser.add_argument(
        '-d', '--discover',
        action='store_true',
        help='Do schema discovery')

    args = parser.parse_args()
    if args.config:
        args.config = load_json(args.config)
    if args.state:
        args.state = load_json(args.state)
    else:
        args.state = {}
    if args.properties:
        args.properties = load_json(args.properties)
    if args.catalog:
        args.catalog = Catalog.load(args.catalog)

    check_config(args.config, required_config_keys)

    return args


def check_config(config, required_keys):
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise Exception("Config is missing required keys: {}".format(missing_keys))


def backoff(exceptions, giveup):
    """Decorates a function to retry up to 5 times using an exponential backoff
    function.

    exceptions is a tuple of exception classes that are retried
    giveup is a function that accepts the exception and returns True to retry
    """
    return backoff_module.on_exception(
        backoff_module.expo,
        exceptions,
        max_tries=5,
        giveup=giveup,
        factor=2)


def exception_is_4xx(exception):
    """Returns True if exception is in the 4xx range."""
    if not hasattr(exception, "response"):
        return False

    if exception.response is None:
        return False

    if not hasattr(exception.response, "status_code"):
        return False

    return 400 <= exception.response.status_code < 500
