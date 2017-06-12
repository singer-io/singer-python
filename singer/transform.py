import datetime
import pendulum
from singer import utils

# pylint: disable=line-too-long
def _transform_object(data, prop_schema, integer_datetime_fmt, path, error_paths):
    result = {}
    successes = []
    for key, value in data.items():
        if key in prop_schema:
            success, subdata, _, error_paths = transform_recur(value, prop_schema[key], integer_datetime_fmt, path + [key], error_paths)
            successes.append(success)
            result[key] = subdata
    return all(successes), result, path, error_paths

def _transform_array(data, item_schema, integer_datetime_fmt, path, error_paths):
    result = []
    successes = []
    for i, row in enumerate(data):
        success, subdata, _, error_paths = transform_recur(row, item_schema, integer_datetime_fmt, path + [i], error_paths)
        successes.append(success)
        result.append(subdata)
    return all(successes), result, path, error_paths

def unix_milliseconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value) * 0.001))

def unix_seconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value)))

def string_to_datetime(value):
    return utils.strftime(pendulum.parse(value))

def _transform_datetime(value, integer_datetime_fmt):
    if integer_datetime_fmt not in [NO_INTEGER_DATETIME_PARSING,
                                    UNIX_SECONDS_INTEGER_DATETIME_PARSING,
                                    UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING]:
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
        else:
            return False, None, path, error_paths + [path]

    elif schema.get("format") == "date-time":
        return True, _transform_datetime(data, integer_datetime_fmt), path, error_paths

    elif typ == "object":
        return _transform_object(data, schema["properties"], integer_datetime_fmt, path, error_paths)

    elif typ == "array":
        return _transform_array(data, schema["items"], integer_datetime_fmt, path, error_paths)

    elif typ == "string":
        if data != None:
            return True, str(data), path, error_paths
        else:
            return False, None, path, error_paths + [path]

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
    success, transformed_data, _, error_paths = transform_recur(data, schema, integer_datetime_fmt, [], [])
    if success:
        return transformed_data
    else:
        raise Exception("Errors at paths {} in data {} for schema {}".format(error_paths, data, schema))

def _transform_anyof(data, schema, integer_datetime_fmt, path, error_paths):
    subschemas = schema["anyOf"]
    subschemas_length = len(subschemas)
    for i, subschema in enumerate(subschemas):
        success, transformed_data, path, error_paths = transform_recur(data, subschema, integer_datetime_fmt, path, error_paths)
        if success:
            return success, transformed_data, path, error_paths
        else:
            if i == (subschemas_length - 1):
                return False, None, path, error_paths + [path]
            else:
                pass

def transform_recur(data, schema, integer_datetime_fmt, path, error_paths):
    """
    This function (and several of its helper functions) returns a tuple:
    (success, data, path, error_paths)
    success is a boolean flag indicating whether data was successfully transformed with schema
    data is the transformed data
    path is the current path in the tree traversal of the data and schema
    error_paths is a list of paths where the data could not be transformed according to the schema
    """

    # NB: This adds support for the `anyOf` keyword, but we do NOT support
    # the follow json schema keywords: `allOf`, `oneOf`, `not`
    if schema.get("anyOf"):
        return _transform_anyof(data, schema, integer_datetime_fmt, path, error_paths)

    types = schema["type"]
    if not isinstance(types, list):
        types = [types]

    if "null" in types:
        types.remove("null")
        types.append("null")

    type_length = len(types)
    for i, typ in enumerate(types):
        try:
            success, data, path, error_paths = _transform(data, typ, schema, integer_datetime_fmt, path, error_paths)
            if success:
                return success, data, path, error_paths
            else:
                if i == (type_length - 1):
                    return False, None, path, error_paths
                else:
                    pass
        except:
            if i == (type_length - 1):
                return False, None, path, error_paths + [path]
            else:
                pass
