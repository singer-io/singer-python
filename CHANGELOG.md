# Changelog

## 5.1.0
  * Improves logging around unparseable datetimes, now warning level instead of error.
  * Adds feature to transformer to respect `selected` and `"inclusion": "unsupported"` metadata if passed in.

## 5.0.15
  * Fix datetime serialization call in `messages.write_record` for `time_extracted` to format consistently across platforms

## 5.0.14
  * Allow transform's string_to_datetime to accept a datetime with timezone and peg at UTC for further processing
  * Implemented cross platform strftime formatting in `utils.strftime`, based on [tap-codat #3](https://github.com/singer-io/tap-codat/pull/3)

## 5.0.6
  * Adds replication_method as a field to the catalog class

## 5.0.5
  * Sets the default format for dates to use %04Y so dates < 1000 are formatted with leading zeroes [#65](https://github.com/singer-io/singer-python/pull/65)
