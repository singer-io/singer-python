from singer import state as st
from typing_extensions import deprecated

@deprecated("Use singer.state.ensure_state_path")
def ensure_bookmark_path(state, path):
    return st.ensure_state_path(state, path)

@deprecated("Use singer.state.write_bookmark")
def write_bookmark(state, tap_stream_id, key, val):
    return st.write_bookmark(state, tap_stream_id, key, val)

@deprecated("Use singer.state.clear_bookmark")
def clear_bookmark(state, tap_stream_id, key):
    return st.clear_bookmark(state, tap_stream_id, key)

@deprecated("Use singer.state.reset_stream")
def reset_stream(state, tap_stream_id):
    return st.reset_stream(state, tap_stream_id)

@deprecated("Use singer.state.get_bookmark")
def get_bookmark(state, tap_stream_id, key, default=None):
    return st.get_bookmark(state, tap_stream_id, key, default)

@deprecated("Use singer.state.set_offset")
def set_offset(state, tap_stream_id, offset_key, offset_value):
    return st.set_offset(state, tap_stream_id, offset_key, offset_value)

@deprecated("Use singer.state.clear_offset")
def clear_offset(state, tap_stream_id):
    return st.clear_offset(state, tap_stream_id)

@deprecated("Use singer.state.get_offset")
def get_offset(state, tap_stream_id, default=None):
    return st.get_offset(state, tap_stream_id, default)

@deprecated("Use singer.state.set_currently_syncing")
def set_currently_syncing(state, tap_stream_id):
    return st.set_currently_syncing(state, tap_stream_id)

@deprecated("Use singer.state.get_currently_syncing")
def get_currently_syncing(state, default=None):
    return st.get_currently_syncing(state, default)

