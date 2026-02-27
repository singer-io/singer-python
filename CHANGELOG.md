# Changelog

## 6.8.0
  * Rename state key `activate_versions` to `versions` in all relevant locations [#194](https://github.com/singer-io/singer-python/pull/194)

## 6.7.0
  * Remove `key` from set_version, get_version, and clear_version state functions [#192](https://github.com/singer-io/singer-python/pull/192)

## 6.6.0
  * Export singer.state functions from singer
  * Rename singer.state.write_bookmark to singer.state.set_bookmark
  * [#190](https://github.com/singer-io/singer-python/pull/190)

## 6.5.0
  * Add `activate_versions` state functions [#188](https://github.com/singer-io/singer-python/pull/188)
  * Deprecates bookmarks.py, functions are moved to state.py

## 6.4.0
  * Update clear_offset to remove offset key from bookmark [#185](https://github.com/singer-io/singer-python/pull/185)

## 6.3.0
  * Support allow_nan in message JSON output [#183](https://github.com/singer-io/singer-python/pull/183)

## 6.2.3
  * Default type for non-standard data types is string [#182](https://github.com/singer-io/singer-python/pull/182)

## 6.2.2
  * Updates json schema generation to not emit dates
  * Handle multiple schemas with anyOf and emit them in a specific order
  * Do not emit error messages when checking multiple schemas and a subsequent schema passes
  * [#179](https://github.com/singer-io/singer-python/pull/179)

## 6.2.1
  * Fixes json schema generation to not treat numbers as dates
  * Fixes json schema generation to handle empty arrays
  * Fixes record transformation to handle fields that could be either formatted string or nested data structure
  * [#177](https://github.com/singer-io/singer-python/pull/177)

## 6.2.0
  * Adds json schema generation [#175](https://github.com/singer-io/singer-python/pull/175)

## 6.1.0
  * Make ensure_ascii Dynamic with Default Set to True in JSON Serialization. Required to handle the special characters [#168](https://github.com/singer-io/singer-python/pull/168)

## 6.0.1
  * Pin backoff and simplejson to any version greater than or equal to the previously allowed version, up to the next major version [#167](https://github.com/singer-io/singer-python/pull/167)

## 6.0.0
  * Bump backoff version to 2.2.1. This version drops support for python 3.5, but adds it for 3.10 [#165](https://github.com/singer-io/singer-python/pull/165)

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
