import datetime
import pendulum
from singer import utils


def _transform_object(data, prop_schema):
    return {k: transform(v, prop_schema[k]) for k, v in data.items() if k in prop_schema}

def _transform_array(data, item_schema):
    return [transform(row, item_schema) for row in data]

def unix_milliseconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value) * 0.001))

def unix_seconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value)))

def string_to_datetime(value):
    return  utils.strftime(pendulum.parse(value))

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

NO_INTEGER_DATETIME_PARSING = 0
UNIX_SECONDS_INTEGER_DATETIME_PARSING = 1
UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING = 2

def _transform(data, typ, schema, integer_datetime_fmt):
    if typ == "null":
        if data is None or data == "":
            return None
        else:
            raise ValueError("Not null")

    elif schema.get("format") == "date-time":
        return _transform_datetime(data, integer_datetime_fmt)

    elif typ == "object":
        return _transform_object(data, schema["properties"])

    elif typ == "array":
        return _transform_array(data, schema["items"])

    elif typ == "string":
        if data:
            return str(data)
        else:
            raise ValueError("Not string")

    elif typ == "integer":
        if isinstance(data, str):
            data = data.replace(',', '')
        return int(data)

    elif typ == "number":
        if isinstance(data, str):
            data = data.replace(',', '')
        return float(data)

    elif typ == "boolean":
        return bool(data)

    else:
        raise Exception("Invalid type: {}".format(typ))

def transform(data, schema, integer_datetime_fmt=NO_INTEGER_DATETIME_PARSING):
    types = schema["type"]
    if not isinstance(types, list):
        types = [types]

    if "null" in types:
        types.remove("null")
        types.append("null")

    for typ in types:
        try:
            return _transform(data, typ, schema, integer_datetime_fmt)
        except:
            pass

    raise Exception("Invalid data: {} does not match {}".format(data, schema))
