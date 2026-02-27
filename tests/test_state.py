import unittest
from singer import state as st

class TestBookmark(unittest.TestCase):
    def test_empty_state(self):
        empty_state = {}

        # Case with no value to fall back on
        self.assertIsNone(st.get_bookmark(empty_state, 'some_stream', 'my_key'))

        # Case with a given default
        self.assertEqual(st.get_bookmark(empty_state, 'some_stream', 'my_key', 'default_value'),
                         'default_value')

    def test_empty_bookmark(self):
        empty_bookmark = {'bookmarks':{}}

        # Case with no value to fall back on
        self.assertIsNone(st.get_bookmark(empty_bookmark, 'some_stream', 'my_key'))

        # Case with a given default
        self.assertEqual(st.get_bookmark(empty_bookmark, 'some_stream', 'my_key', 'default_value'),
                         'default_value')

    def test_non_empty_state(self):
        stream_id_1 = 'customers'
        bookmark_key_1 = 'datetime'
        bookmark_val_1 = 123456789

        non_empty_state = {
            'bookmarks' : {
                stream_id_1 : {
                    bookmark_key_1 : bookmark_val_1
                }
            }
        }

        #
        # Cases with no value to fall back on
        #

        # Bad stream, bad key
        self.assertIsNone(st.get_bookmark(non_empty_state, 'some_stream', 'my_key'))

        # Good stream, bad key
        self.assertIsNone(st.get_bookmark(non_empty_state, stream_id_1, 'my_key'))

        # Good stream, good key
        self.assertEqual(st.get_bookmark(non_empty_state, stream_id_1, bookmark_key_1),
                         bookmark_val_1)

        #
        # Cases with a given default
        #

        # Bad stream, bad key
        self.assertEqual(st.get_bookmark(non_empty_state, 'some_stream', 'my_key', 'default_value'),
                         'default_value')

        # Bad stream, good key
        self.assertEqual(st.get_bookmark(non_empty_state, 'some_stream', bookmark_key_1, 'default_value'),
                         'default_value')

        # Good stream, bad key
        self.assertEqual(st.get_bookmark(non_empty_state, stream_id_1, 'my_key', 'default_value'),
                         'default_value')

        # Good stream, good key
        self.assertEqual(st.get_bookmark(non_empty_state, stream_id_1, bookmark_key_1, 'default_value'),
                         bookmark_val_1)

    def test_set_bookmark(self):
        stream_id_1 = 'customers'
        bookmark_key_1 = 'datetime'
        bookmark_val_1 = 123456789

        result = st.set_bookmark({'bookmarks': {stream_id_1: {bookmark_key_1: 'old-value'}}}, stream_id_1, bookmark_key_1, bookmark_val_1)
        self.assertEqual(result, {'bookmarks': {stream_id_1: {bookmark_key_1: bookmark_val_1}}})

    def test_clear_bookmark(self):
        stream_id_1 = 'customers'
        bookmark_key_1 = 'datetime'
        bookmark_val_1 = 123456789

        result = st.clear_bookmark({'bookmarks': {stream_id_1: {bookmark_key_1: bookmark_val_1}}}, stream_id_1, bookmark_key_1)
        self.assertEqual(result, {'bookmarks': {stream_id_1: {}}})


class TestOffset(unittest.TestCase):
    def test_empty_state(self):
        empty_state = {}

        # Case with no value to fall back on
        self.assertIsNone(st.get_offset(empty_state, 'some_stream'))

        # Case with a given default
        self.assertEqual(st.get_offset(empty_state, 'some_stream', 'default_value'),
                         'default_value')

    def test_empty_bookmark(self):
        empty_bookmark = {'bookmarks':{}}

        # Case with no value to fall back on
        self.assertIsNone(st.get_offset(empty_bookmark, 'some_stream'))

        # Case with a given default
        self.assertEqual(st.get_offset(empty_bookmark, 'some_stream', 'default_value'),
                         'default_value')

    def test_non_empty_state(self):
        stream_id_1 = 'customers'
        bookmark_key_1 = 'datetime'
        bookmark_val_1 = 123456789
        offset_val = 'fizzy water'

        non_empty_state = {
            'bookmarks' : {
                stream_id_1 : {
                    bookmark_key_1 : bookmark_val_1,
                    'offset' : offset_val
                }
            }
        }

        #
        # Cases with no value to fall back on
        #

        # Bad stream
        self.assertIsNone(st.get_offset(non_empty_state, 'some_stream'))

        # Good stream
        self.assertEqual(st.get_offset(non_empty_state, stream_id_1),
                         offset_val)

        #
        # Case with a given default
        #

        # Bad stream
        self.assertEqual(st.get_offset(non_empty_state, 'some_stream', 'default_value'),
                         'default_value')

        # Good stream
        self.assertEqual(st.get_offset(non_empty_state, stream_id_1, 'default_value'),
                         offset_val)

    def test_set_offset(self):
        stream_id_1 = 'customers'
        offset_key_1 = 'datetime'
        offset_val_1 = 123456789

        result = st.set_offset({'bookmarks': {stream_id_1: {'offset': {offset_key_1: 'old-value'}}}}, stream_id_1, offset_key_1, offset_val_1)
        self.assertEqual(result, {'bookmarks': {stream_id_1: {'offset': {offset_key_1: offset_val_1}}}})

    def test_clear_offset(self):
        stream_id_1 = 'customers'
        offset_key_1 = 'datetime'
        offset_val_1 = 123456789

        result = st.clear_offset({'bookmarks': {stream_id_1: {'offset': {offset_key_1: offset_val_1}}}}, stream_id_1)
        self.assertEqual(result, {'bookmarks': {stream_id_1: {}}})


class TestCurrentlySyncing(unittest.TestCase):
    def test_empty_state(self):
        empty_state = {}

        # Case with no value to fall back on
        self.assertIsNone(st.get_currently_syncing(empty_state))

        # Case with a given default
        self.assertEqual(st.get_currently_syncing(empty_state, 'default_value'),
                         'default_value')

    def test_non_empty_state(self):
        stream_id_1 = 'customers'
        bookmark_key_1 = 'datetime'
        bookmark_val_1 = 123456789
        offset_val = 'fizzy water'

        non_empty_state = {
            'bookmarks' : {
                stream_id_1 : {
                    bookmark_key_1 : bookmark_val_1,
                    'offset' : offset_val
                }
            },
            'currently_syncing' : stream_id_1
        }

        # Case with no value to fall back on
        self.assertEqual(st.get_currently_syncing(non_empty_state),
                         stream_id_1)

        # Case with a given default
        self.assertEqual(st.get_currently_syncing(non_empty_state, 'default_value'),
                         stream_id_1)

    def test_set_currently_syncing(self):
        result = st.set_currently_syncing({'currently_syncing': 'foo'}, 'bar')
        self.assertEqual(result, {'currently_syncing': 'bar'})


class TestVersions(unittest.TestCase):
    def test_empty_state(self):
        empty_state = {}

        # Case with no value to fall back on
        self.assertIsNone(st.get_version(empty_state, 'some_stream'))

        # Case with a given default
        self.assertEqual(st.get_version(empty_state, 'some_stream', 'default_value'),
                         'default_value')

    def test_empty_versions(self):
        empty_versions = {'versions':{}}

        # Case with no value to fall back on
        self.assertIsNone(st.get_version(empty_versions, 'some_stream'))

        # Case with a given default
        self.assertEqual(st.get_version(empty_versions, 'some_stream', 'default_value'),
                         'default_value')

    def test_non_empty_state(self):
        stream_id_1 = 'customers'
        version_val_1 = 123456789

        non_empty_state = {
            'versions' : {
                stream_id_1 : version_val_1
            }
        }

        #
        # Cases with no value to fall back on
        #

        # Bad stream
        self.assertIsNone(st.get_version(non_empty_state, 'some_stream'))

        # Good stream
        self.assertEqual(st.get_version(non_empty_state, stream_id_1),
                         version_val_1)

        #
        # Cases with a given default
        #

        # Bad stream
        self.assertEqual(st.get_version(non_empty_state, 'some_stream', 'default_value'),
                         'default_value')

        # Good stream
        self.assertEqual(st.get_version(non_empty_state, stream_id_1, 'default_value'),
                         version_val_1)

    def test_set_version(self):
        stream_id_1 = 'customers'
        version_val_1 = 123456789

        result = st.set_version({'versions': {stream_id_1: 'old-value'}}, stream_id_1, version_val_1)
        self.assertEqual(result, {'versions': {stream_id_1: version_val_1}})

    def test_clear_version(self):
        stream_id_1 = 'customers'
        version_val_1 = 123456789

        result = st.clear_version({'versions': {stream_id_1: version_val_1}}, stream_id_1)
        self.assertEqual(result, {'versions': {}})
