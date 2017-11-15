import collections

def paths(s, base=None):
    '''Walk a data structure and return a list of (path, value) tuples, where
    each path is the path to a leaf node in the data structure and the
    value is the value it points to. Each path will be a tuple of strings
    and integers.

    '''
    if base is None:
        base = ()

    result = []
    if isinstance(s, dict):
        for k, v in sorted(s.items()):
            result.extend(paths(v, base + (k,)))

    elif isinstance(s, list):
        for i, v in enumerate(s):
            result.extend(paths(v, base + (i,)))

    else:
        result.append((base, s))

    return result

Change = collections.namedtuple('Change', ['path', 'oldval', 'newval'])
Remove = collections.namedtuple('Remove', ['path', 'oldval'])
Add    = collections.namedtuple('Add', ['path', 'newval'])

def diff(s1, s2):
    '''Compare two states, returning a list of Add, Change, and Remove
    objects.

    Add(path, newval) means path exists in s2 but not s1 and its value in
    s2 is newval.

    Change(path, oldval, newval) means that path exists in both s1 and s2
    but has different values. oldval is the val in s1 and newval is the
    value in s2.
    
    Remove(path, oldval) means the path exists in s1 but not in s2, and
    the value in s1 is oldval.

    '''    
    dict1 = {k: v for (k, v) in paths(s1)}
    dict2 = {k: v for (k, v) in paths(s2)}

    all_paths = set()
    all_paths.update(set(dict1.keys()))
    all_paths.update(set(dict2.keys()))

    result = []
    for path in sorted(all_paths):
        if path in dict1:
            if path in dict2:
                if dict1[path] == dict2[path]:
                    pass
                else:
                    result.append(Change(path, dict1[path], dict2[path]))
            else:
                result.append(Remove(path, dict1[path]))
        else:
            result.append(Add(path, dict2[path]))
    return result
