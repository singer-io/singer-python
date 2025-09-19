# Changelog

## 5.14.0
  * Adds json schema generation [#172](https://github.com/singer-io/singer-python/pull/172)

## 5.13.2
  * Bump backoff version to 1.10.0

## 5.13.1
  * Switch `setup.cfg` to use underscore instead of dash because setuptools has deprecated anything other than lower_snake_case. See [setuptools issue](https://github.com/pypa/setuptools/issues/4910) for more context.

## 5.13.0
  * Add support for dev mode argument parsing [#158](https://github.com/singer-io/singer-python/pull/158)

## 5.12.2
  * Removes pinned `pytz` version [#152](https://github.com/singer-io/singer-python/pull/152)

## 5.12.1
  * Removes normalize function from `singer.decimal` to avoid scientific notation [#146](https://github.com/singer-io/singer-python/pull/146)

## 5.12.0
  * Added support for `singer.decimal` types to transformer [#125](https://github.com/singer-io/singer-python/pull/125)

## 5.11.0
  * Make `utils.handle_top_exception()` critically log each line of the exception separately so each line is prepended with `CRITICAL` [#141](https://github.com/singer-io/singer-python/pull/141)

## 5.10.0
  * Add exception classes [#138](https://github.com/singer-io/singer-python/pull/138)

## 5.9.1
  * Add nested schema support to Transformer's `filter_data_by_metadata` function [#130](https://github.com/singer-io/singer-python/pull/130)

## 5.8.1
  * Allow empty lists for `key-properties` and `valid-replication-keys` in `get_standard_metadata` [#106](https://github.com/singer-io/singer-python/pull/106)

## 5.7.0
  * Bumping backoff dependency to 1.8.0 for aiohttp support
  * Added `get_selected_streams` to the `Catalog` class that orders streams returned with `currently_syncing` from state (if present) at the front of the list. [#100](https://github.com/singer-io/singer-python/pull/100)
  * Added helper called `write_catalog` for use in discovery mode [#101](https://github.com/singer-io/singer-python/pull/101)

## 5.6.1
  * Retain argument paths in `parse_args` [#88](https://github.com/singer-io/singer-python/pull/88)

## 5.5.0
  * Add the ability to specify a default value when getting a bookmark [#95](https://github.com/singer-io/singer-python/pull/95)

## 5.4.1
  * Resolve JSON Schema refs when the schema contains an `anyOf` element [#93](https://github.com/singer-io/singer-python/pull/93)

## 5.4.0
  * Support for schema objects that contain `patternProperties` [#92](https://github.com/singer-io/singer-python/pull/92)

## 5.2.2
  * Transform now treats empty object schemas as *all* properties [#77](https://github.com/singer-io/singer-python/pull/77)

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
