import datetime
import pendulum
from singer import utils


NO_INTEGER_DATETIME_PARSING = "no-integer-datetime-parsing"
UNIX_SECONDS_INTEGER_DATETIME_PARSING = "unix-seconds-integer-datetime-parsing"
UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING = "unix-milliseconds-integer-datetime-parsing"

VALID_DATETIME_FORMATS = [
    NO_INTEGER_DATETIME_PARSING,
    UNIX_SECONDS_INTEGER_DATETIME_PARSING,
    UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING,
]


def string_to_datetime(value):
    return utils.strftime(pendulum.parse(value))


def unix_milliseconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value) * 0.001))


def unix_seconds_to_datetime(value):
    return utils.strftime(datetime.datetime.utcfromtimestamp(int(value)))


class SchemaMismatch(Exception):
    def __init__(self, errors):
        msg = "Errors during transform\n\t{}".format("\n\t".join(e.tostr() for e in errors))
        super(SchemaMismatch, self).__init__(msg)


class Error:
    def __init__(self, path, data, schema=None):
        self.path = path
        self.data = data
        self.schema = schema

    def tostr(self):
        path = ".".join(map(str, self.path))
        if self.schema:
            msg = "does not match {}".format(self.schema)
        else:
            msg = "not in schema"

        return "{}: {} {}".format(path, self.data, msg)


class Transformer:
    def __init__(self, integer_datetime_fmt=NO_INTEGER_DATETIME_PARSING, pre_hook=None):
        self.integer_datetime_fmt = integer_datetime_fmt
        self.pre_hook = pre_hook
        self._errors = []

    def transform(self, data, schema):
        success, transformed_data = self.transform_recur(data, schema, [])
        if not success:
            raise SchemaMismatch(self._errors)

        return transformed_data

    def transform_recur(self, data, schema, path):
        if "anyOf" in schema:
            return self._transform_anyof(data, schema, path)

        types = schema["type"]
        if not isinstance(types, list):
            types = [types]

        if "null" in types:
            types.remove("null")
            types.append("null")

        types_len = len(types)
        for i, typ in enumerate(types):
            try:
                success, transformed_data = self._transform(data, typ, schema, path)
                if success:
                    return success, transformed_data
                else:
                    if i == (types_len - 1):
                        if "object" not in types and "array" not in types:
                            self._errors.append(Error(path, data, schema))
                        return False, None
                    else:
                        pass
            except:
                if i == (types_len - 1):
                    if "object" not in types and "array" not in types:
                        self._errors.append(Error(path, data, schema))
                    return False, None
                else:
                    pass

    def _transform_anyof(self, data, schema, path):
        subschemas = schema['anyOf']
        subschemas_len = len(subschemas)
        for i, subschema in enumerate(subschemas):
            success, transformed_data = self.transform_recur(data, subschema, path)
            if success:
                return success, transformed_data
            else:
                if i == (subschemas_len - 1):
                    return False, None
                else:
                    pass

    def _transform_object(self, data, schema, path):
        result = {}
        successes = []
        for key, value in data.items():
            if key in schema:
                success, subdata = self.transform_recur(value, schema[key], path + [key])
                successes.append(success)
                result[key] = subdata
            else:
                # Pass on fields not in schema
                result[key] = value

        return all(successes), result

    def _transform_array(self, data, schema, path):
        result = []
        successes = []
        for i, row in enumerate(data):
            success, subdata = self.transform_recur(row, schema, path + [i])
            successes.append(success)
            result.append(subdata)

        return all(successes), result

    def _transform_datetime(self, value):
        if self.integer_datetime_fmt not in VALID_DATETIME_FORMATS:
            raise Exception("Invalid integer datetime parsing option")

        if self.integer_datetime_fmt == NO_INTEGER_DATETIME_PARSING:
            return string_to_datetime(value)
        else:
            try:
                if self.integer_datetime_fmt == UNIX_SECONDS_INTEGER_DATETIME_PARSING:
                    return unix_seconds_to_datetime(value)
                else:
                    return unix_milliseconds_to_datetime(value)
            except:
                return string_to_datetime(value)

    def _transform(self, data, typ, schema, path):
        if self.pre_hook:
            data = self.pre_hook(data, typ, schema)

        if typ == "null":
            if data is None or data == "":
                return True, None
            else:
                return False, None

        elif schema.get("format") == "date-time":
            return True, self._transform_datetime(data)

        elif typ == "object":
            return self._transform_object(data, schema["properties"], path)

        elif typ == "array":
            return self._transform_array(data, schema["items"], path)

        elif typ == "string":
            if data != None:
                return True, str(data)
            else:
                return False, None

        elif typ == "integer":
            if isinstance(data, str):
                data = data.replace(",", "")

            return True, int(data)

        elif typ == "number":
            if isinstance(data, str):
                data = data.replace(",", "")

            return True, float(data)

        elif typ == "boolean":
            if isinstance(data, str) and data.lower() == "false":
                return True, False

            return True, bool(data)

        else:
            return False, None


def transform(data, schema, integer_datetime_fmt=NO_INTEGER_DATETIME_PARSING, pre_hook=None):
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

    The pre_hook should be a callable that takes data, type, and schema and
    returns the transformed data to be fed into the _transform function.
    """
    transformer = Transformer(integer_datetime_fmt, pre_hook)
    return transformer.transform(data, schema)
