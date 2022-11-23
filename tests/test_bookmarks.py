from copy import copy
import unittest
from singer.bookmarks import State


class TestGetBookmark(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()

        # Case with no value to fall back on
        self.assertIsNone(empty_state.get_bookmark("some_stream", "my_key"))

        # Case with a given default
        self.assertEqual(
            empty_state.get_bookmark("some_stream", "my_key", "default_value"),
            "default_value",
        )

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})

        # Case with no value to fall back on
        self.assertIsNone(empty_bookmark.get_bookmark("some_stream", "my_key"))

        # Case with a given default
        self.assertEqual(
            empty_bookmark.get_bookmark("some_stream", "my_key", "default_value"),
            "default_value",
        )

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        bookmarks = {stream_id_1: {bookmark_key_1: bookmark_val_1}}

        non_empty_state = State(bookmarks=bookmarks)

        #
        # Cases with no value to fall back on
        #

        # Bad stream, bad key
        self.assertIsNone(non_empty_state.get_bookmark("some_stream", "my_key"))

        # Good stream, bad key
        self.assertIsNone(non_empty_state.get_bookmark(stream_id_1, "my_key"))

        # Good stream, good key
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )

        #
        # Cases with a given default
        #

        # Bad stream, bad key
        self.assertEqual(
            non_empty_state.get_bookmark("some_stream", "my_key", "default_value"),
            "default_value",
        )

        # Bad stream, good key
        self.assertEqual(
            non_empty_state.get_bookmark(
                "some_stream", bookmark_key_1, "default_value"
            ),
            "default_value",
        )

        # Good stream, bad key
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, "my_key", "default_value"),
            "default_value",
        )

        # Good stream, good key
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1, "default_value"),
            bookmark_val_1,
        )


class TestWriteBookmark(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()
        self.assertIsNone(empty_state.get_bookmark("some_stream", "my_key"))
        empty_state.write_bookmark("some_stream", "my_key", "val")
        self.assertEqual(empty_state.get_bookmark("some_stream", "my_key"), "val")

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})
        self.assertIsNone(empty_bookmark.get_bookmark("some_stream", "my_key"))
        empty_bookmark.write_bookmark("some_stream", "my_key", "val")
        self.assertEqual(empty_bookmark.get_bookmark("some_stream", "my_key"), "val")

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        bookmark_val_2 = 0
        bookmarks = {stream_id_1: {bookmark_key_1: bookmark_val_1}}

        non_empty_state = State(bookmarks=bookmarks)

        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )
        non_empty_state.write_bookmark(stream_id_1, bookmark_key_1, bookmark_val_2)
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_2
        )


class TestClearBookmark(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()
        empty_state.clear_bookmark("some_stream", "key")
        self.assertIsNone(empty_state.get_bookmark("some_stream", "my_key"))

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})
        empty_bookmark.clear_bookmark("some_stream", "key")
        self.assertIsNone(empty_bookmark.get_bookmark("some_stream", "my_key"))

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        bookmarks = {stream_id_1: {bookmark_key_1: bookmark_val_1}}

        #
        # Cases with no value to fall back on
        #

        # Bad stream, bad key
        non_empty_state = State(bookmarks=bookmarks)
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )
        non_empty_state.clear_bookmark("some_stream", "some_key")
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )

        # Good stream, bad key
        non_empty_state = State(bookmarks=bookmarks)
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )
        non_empty_state.clear_bookmark(stream_id_1, "some_key")
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )

        # Good stream, good key
        non_empty_state = State(bookmarks=bookmarks)
        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )
        non_empty_state.clear_bookmark(stream_id_1, bookmark_key_1)
        self.assertIsNone(non_empty_state.get_bookmark(stream_id_1, bookmark_key_1))


class TestClearStream(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()
        self.assertFalse("some_stream" in empty_state.bookmarks)
        empty_state.reset_stream("some_stream")
        self.assertTrue("some_stream" in empty_state.bookmarks)
        self.assertIsNone(empty_state.bookmarks["some_stream"] or None)

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})
        self.assertFalse("some_stream" in empty_bookmark.bookmarks)
        empty_bookmark.reset_stream("some_stream")
        self.assertTrue("some_stream" in empty_bookmark.bookmarks)
        self.assertIsNone(empty_bookmark.bookmarks["some_stream"] or None)

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        bookmarks = {stream_id_1: {bookmark_key_1: bookmark_val_1}}

        non_empty_state = State(bookmarks=bookmarks)

        self.assertEqual(
            non_empty_state.get_bookmark(stream_id_1, bookmark_key_1), bookmark_val_1
        )
        non_empty_state.reset_stream(stream_id_1)
        self.assertTrue(stream_id_1 in non_empty_state.bookmarks)
        self.assertIsNone(non_empty_state.get_bookmark(stream_id_1, bookmark_key_1))


class TestGetOffset(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()

        # Case with no value to fall back on
        self.assertIsNone(empty_state.get_offset("some_stream", "offset_key"))

        # Case with a given default
        self.assertEqual(
            empty_state.get_offset("some_stream", "offset_key", "default_value"),
            "default_value",
        )

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})

        # Case with no value to fall back on
        self.assertIsNone(empty_bookmark.get_offset("some_stream", "offset_key"))

        # Case with a given default
        self.assertEqual(
            empty_bookmark.get_offset("some_stream", "offset_key", "default_value"),
            "default_value",
        )

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        offset_key = "key"
        offset_val = "fizzy water"

        bookmarks = {
            stream_id_1: {
                bookmark_key_1: bookmark_val_1,
                "offset": {offset_key: offset_val},
            }
        }

        non_empty_state = State(bookmarks=bookmarks)

        #
        # Cases with no value to fall back on
        #

        # Bad stream
        self.assertIsNone(non_empty_state.get_offset("some_stream", offset_key))

        # Good stream
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key), offset_val
        )

        #
        # Case with a given default
        #

        # Bad stream
        self.assertEqual(
            non_empty_state.get_offset("some_stream", offset_key, "default_value"),
            "default_value",
        )

        # Good stream
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key, "default_value"),
            offset_val,
        )


class TestClearOffset(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()
        empty_state.clear_offset("some_stream")
        self.assertIsNone(empty_state.get_offset("some_stream", "offset_key"))

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})
        empty_bookmark.clear_offset("some_stream")
        self.assertIsNone(empty_bookmark.get_offset("some_stream", "offset_key"))

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        offset_key = "key"
        offset_val = "fizzy water"

        bookmarks = {
            stream_id_1: {
                bookmark_key_1: bookmark_val_1,
                "offset": {offset_key: offset_val},
            }
        }

        non_empty_state = State(bookmarks=bookmarks)

        # Bad stream
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key), offset_val
        )
        non_empty_state.clear_offset("some_stream")
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key), offset_val
        )

        # Good stream
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key), offset_val
        )
        non_empty_state.clear_offset(stream_id_1)
        self.assertIsNone(non_empty_state.get_offset(stream_id_1, offset_key))


class TestSetOffset(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()
        empty_state.set_offset("some_stream", "offset_key", "offset_value")
        self.assertEqual(
            empty_state.get_offset("some_stream", "offset_key"), "offset_value"
        )

    def test_empty_bookmark(self):
        empty_bookmark = State(bookmarks={})
        empty_bookmark.set_offset("some_stream", "offset_key", "offset_value")
        self.assertEqual(
            empty_bookmark.get_offset("some_stream", "offset_key"), "offset_value"
        )

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        offset_key_1 = "offset_key_1"
        offset_key_2 = "offset_key_2"
        offset_val_1 = "fizzy water"
        offset_val_2 = "still water"

        bookmarks = {
            stream_id_1: {
                bookmark_key_1: bookmark_val_1,
                "offset": {"offset_key_1": offset_val_1,},
            }
        }

        non_empty_state = State(bookmarks=bookmarks)

        # Test setting new key
        non_empty_state.set_offset(stream_id_1, offset_key_2, offset_val_2)
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key_1), offset_val_1
        )
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key_2), offset_val_2
        )

        # Test overwriting key
        non_empty_state.set_offset(stream_id_1, offset_key_1, offset_val_2)
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key_1), offset_val_2
        )
        self.assertEqual(
            non_empty_state.get_offset(stream_id_1, offset_key_2), offset_val_2
        )


class TestGetCurrentlySyncing(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()

        # Case with no value to fall back on
        self.assertIsNone(empty_state.get_currently_syncing())

        # Case with a given default
        self.assertEqual(
            empty_state.get_currently_syncing("default_value"), "default_value"
        )

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        offset_val = "fizzy water"

        bookmarks = {
            stream_id_1: {bookmark_key_1: bookmark_val_1, "offset": offset_val}
        }

        non_empty_state = State(bookmarks=bookmarks, currently_syncing=stream_id_1)

        # Case with no value to fall back on
        self.assertEqual(non_empty_state.get_currently_syncing(), stream_id_1)

        # Case with no value to fall back on
        self.assertEqual(
            non_empty_state.get_currently_syncing("default_value"), stream_id_1
        )


class TestSetCurrentlySyncing(unittest.TestCase):
    def test_empty_state(self):
        empty_state = State()

        self.assertIsNone(empty_state.get_currently_syncing())
        empty_state.set_currently_syncing("some_stream")
        self.assertEqual(empty_state.get_currently_syncing(), "some_stream")

    def test_non_empty_state(self):
        stream_id_1 = "customers"
        bookmark_key_1 = "datetime"
        bookmark_val_1 = 123456789
        offset_key = "key"
        offset_val = "fizzy water"

        bookmarks = {
            stream_id_1: {
                bookmark_key_1: bookmark_val_1,
                "offset": {offset_key: offset_val},
            }
        }

        non_empty_state = State(bookmarks=bookmarks, currently_syncing=stream_id_1)

        self.assertEqual(non_empty_state.get_currently_syncing(), stream_id_1)

        non_empty_state.set_currently_syncing("some_stream")
        self.assertEqual(non_empty_state.get_currently_syncing(), "some_stream")


class TestToDictAndFromDict(unittest.TestCase):

    bookmarks = {
        "stream_1": {"stream_1_key_1": 1, "stream_1_key_2": "2019-02-01T00:00:00Z"},
        "stream_2": {
            "stream_2_key_1": 2,
            "stream_2_key_2": "2019-03-01T00:00:00Z",
            "offset": {"offset_1": 1},
        },
    }

    dict_form = {"bookmarks": bookmarks, "currently_syncing": "stream_1"}

    obj_form = State(bookmarks=bookmarks, currently_syncing="stream_1")

    def test_from_dict(self):
        dict_form = self.dict_form.copy()
        obj_form = copy(self.obj_form)

        # With currently_syncing
        self.assertEqual(obj_form, State.from_dict(dict_form))

        # # Without currently_syncing
        del dict_form["currently_syncing"]
        obj_form.set_currently_syncing(None)
        self.assertEqual(obj_form, State.from_dict(dict_form))

    def test_to_dict(self):
        dict_form = self.dict_form.copy()
        obj_form = copy(self.obj_form)

        # With currently_syncing
        self.assertEqual(self.dict_form, self.obj_form.to_dict())

        # # Without currently_syncing
        del dict_form["currently_syncing"]
        obj_form.set_currently_syncing(None)
        self.assertEqual(self.dict_form, self.obj_form.to_dict())
