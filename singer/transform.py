import datetime
import pendulum
from copy import deepcopy
from singer import utils


def _transform_object(data, prop_schema, integer_datetime_fmt, path, error_paths):
    result = {}
    successes = []
    for k, v in data.items():
        success, data, _, error_paths = transform_recur(v, prop_schema[k], integer_datetime_fmt, path + [k], error_paths)
        successes.append(success)
        result[k] = data
    return all(successes), result, path, error_paths

def _transform_array(data, item_schema, integer_datetime_fmt, path, error_paths):
    result = []
    successes = []
    for i, row in enumerate(data):
        success, data, _, error_paths = transform_recur(row, item_schema, integer_datetime_fmt, path + [i], error_paths)
        successes.append(success)
        result.append(data)
    return all(successes), result, path, error_paths

def unix_milliseconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value) * 0.001))

def unix_seconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value)))

def string_to_datetime(value):
    return  utils.strftime(pendulum.parse(value))

def _transform_datetime(value, integer_datetime_fmt, path, error_paths):
    if integer_datetime_fmt not in [NO_INTEGER_DATETIME_PARSING,
                                    UNIX_SECONDS_INTEGER_DATETIME_PARSING,
                                    UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING]:
        #return False, None, path, error_paths
        raise Exception("Invalid integer datetime parsing option")

    if integer_datetime_fmt == NO_INTEGER_DATETIME_PARSING:
        return string_to_datetime(value)
    else:
        try:
            if integer_datetime_fmt == UNIX_SECONDS_INTEGER_DATETIME_PARSING:
                return unix_seconds_to_datetime(value)
            elif integer_datetime_fmt == UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING:
                return unix_milliseconds_to_datetime(value)
        except:
            return string_to_datetime(value)

NO_INTEGER_DATETIME_PARSING = "no-integer-datetime-parsing"
UNIX_SECONDS_INTEGER_DATETIME_PARSING = "unix-seconds-integer-datetime-parsing"
UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING = "unix-milliseconds-integer-datetime-parsing"

def _transform(data, typ, schema, integer_datetime_fmt, path, error_paths):
    if typ == "null":
        if data is None or data == "":
            return True, None, path, error_paths
            #return None
        else:
            return False, None, path, error_paths + [path]
            #raise ValueError("Not null")

    elif schema.get("format") == "date-time":
        return True, _transform_datetime(data, integer_datetime_fmt, path, error_paths), path, error_paths

    elif typ == "object":
        return _transform_object(data, schema["properties"], integer_datetime_fmt, path, error_paths)

    elif typ == "array":
        return _transform_array(data, schema["items"], integer_datetime_fmt, path, error_paths)

    elif typ == "string":
        if data != None:
            return True, str(data), path, error_paths
        else:
            return False, None, path, error_paths + [path]
            #raise ValueError("Not string")

    elif typ == "integer":
        if isinstance(data, str):
            data = data.replace(',', '')
        return True, int(data), path, error_paths

    elif typ == "number":
        if isinstance(data, str):
            data = data.replace(',', '')
        return True, float(data), path, error_paths

    elif typ == "boolean":
        return True, bool(data), path, error_paths

    else:
        return False, None, path, error_paths + [path]
    # TODO: don't swallow this
        #raise Exception("Invalid type: {}".format(typ))

def transform(data, schema, integer_datetime_fmt=NO_INTEGER_DATETIME_PARSING):
    """
    Applies schema (and integer_datetime_fmt, if supplied) to data, transforming
    each field in data to the type specified in schema. If no type matches a
    data field, this throws an Exception.

    This applies types in order with the exception of 'null', which is always
    applied last.

    The valid types are: integer, number, boolean, array, object, null, string,
    and string with date-time format.

    If an integer_datetime_fmt is supplied, integer values in fields with date-
    time formats are appropriately parsed as unix seconds or unix milliseconds.
    """
    print("transform called! {} {}".format(data, schema))
    success, data, path, error_paths = transform_recur(data, schema, integer_datetime_fmt, [], [])
    print("Out of transform_recur now! {} {} {} {}".format(success, data, path, error_paths))
    if success:
        return data
    else:
        raise Exception("Errors at paths {} in data {} for schema {}".format(error_paths, data, schema))

def transform_recur(data, schema, integer_datetime_fmt, path, error_paths):
    types = schema["type"]
    if not isinstance(types, list):
        types = [types]

    if "null" in types:
        types.remove("null")
        types.append("null")

    type_length = len(types)
    for i, typ in enumerate(types):
        print("Trying type {} ...".format(typ))
        try:
            success, data, path, error_paths = _transform(data, typ, schema, integer_datetime_fmt, path, error_paths)
            if success:
                return success, data, path, error_paths
            else:
                if i == (type_length - 1):
                    print("Failure {} {}".format(path, error_paths))
                    return False, None, path, error_paths
                else:
                    pass
        except Exception as e:
            if i == (type_length - 1):
                # TODO: this swallows the exception. Forward it along instead?
                print("error_path is {}".format(error_paths))
                print("Exception1 caught: {}".format(e))
                return False, None, path, error_paths + [path]
                #raise Exception("CHECK: Invalid data at leaf error path {}: {} does not match {}".format(error_path, data, schema))
            else:
                print("Exception2 caught: {}".format(e))
                pass



    raise Exception("SHOULDN'T HAPPEN!!!!! Invalid data at error path {}: {} does not match {}".format(error_paths, data, schema))
