def paths(s, base=None):
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

