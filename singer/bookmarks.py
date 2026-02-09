from singer import state as st

## Note - This file is deprecated, use state.py functions.

def ensure_bookmark_path(state, path):
    return st.ensure_state_path(state, path)

def write_bookmark(state, tap_stream_id, key, val):
    return st.write_bookmark(state, tap_stream_id, key, val)

def clear_bookmark(state, tap_stream_id, key):
    return st.clear_bookmark(state, tap_stream_id, key)

def reset_stream(state, tap_stream_id):
    return st.reset_stream(state, tap_stream_id)

def get_bookmark(state, tap_stream_id, key, default=None):
    return st.get_bookmark(state, tap_stream_id, key, default)

def set_offset(state, tap_stream_id, offset_key, offset_value):
    return st.set_offset(state, tap_stream_id, offset_key, offset_value)

def clear_offset(state, tap_stream_id):
    return st.clear_offset(state, tap_stream_id)

def get_offset(state, tap_stream_id, default=None):
    return st.get_offset(state, tap_stream_id, default)

def set_currently_syncing(state, tap_stream_id):
    return st.set_currently_syncing(state, tap_stream_id)

def get_currently_syncing(state, default=None):
    return st.get_currently_syncing(state, default)
