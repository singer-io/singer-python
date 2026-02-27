def ensure_state_path(state, path):
    submap = state
    for path_component in path:
        if submap.get(path_component) is None:
            submap[path_component] = {}

        submap = submap[path_component]
    return state

def set_bookmark(state, tap_stream_id, key, val):
    state = ensure_state_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id][key] = val
    return state

def clear_bookmark(state, tap_stream_id, key):
    state = ensure_state_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id].pop(key, None)
    return state

def reset_stream(state, tap_stream_id):
    state = ensure_state_path(state, ['bookmarks', tap_stream_id])
    state['bookmarks'][tap_stream_id] = {}
    if 'versions' in state:
        state = ensure_state_path(state, ['versions', tap_stream_id])
        state['versions'][tap_stream_id] = {}
    return state

def get_bookmark(state, tap_stream_id, key, default=None):
    return state.get('bookmarks', {}).get(tap_stream_id, {}).get(key, default)

def set_offset(state, tap_stream_id, offset_key, offset_value):
    state = ensure_state_path(state, ['bookmarks', tap_stream_id, "offset", offset_key])
    state['bookmarks'][tap_stream_id]["offset"][offset_key] = offset_value
    return state

def clear_offset(state, tap_stream_id):
    return clear_bookmark(state, tap_stream_id, "offset")

def get_offset(state, tap_stream_id, default=None):
    return state.get('bookmarks', {}).get(tap_stream_id, {}).get("offset", default)

def set_currently_syncing(state, tap_stream_id):
    state['currently_syncing'] = tap_stream_id
    return state

def get_currently_syncing(state, default=None):
    return state.get('currently_syncing', default)

def set_version(state, tap_stream_id, val):
    state = ensure_state_path(state, ['versions', tap_stream_id])
    state['versions'][tap_stream_id] = val
    return state

def clear_version(state, tap_stream_id):
    state = ensure_state_path(state, ['versions', tap_stream_id])
    state['versions'].pop(tap_stream_id, None)
    return state

def get_version(state, tap_stream_id, default=None):
    return state.get('versions', {}).get(tap_stream_id, default)
