def deserialize(raw_metadata):
    return {tuple(breadcrumb): metadata for breadcrumb, metadata in raw_metadata}

def serialize(compiled_metadata):
    return list(compiled_metadata.items())

def delete(compiled_metadata, breadcrumb, k):
    del compiled_metadata[breadcrumb][k]

def write(compiled_metadata, breadcrumb, k, val):
    if val is None:
        raise Exception()
    if breadcrumb in compiled_metadata:
        compiled_metadata.get(breadcrumb).update({k: val})
    else:
        compiled_metadata[breadcrumb] = {k: val}
    return compiled_metadata

def get(compiled_metadata, breadcrumb, k):
    return compiled_metadata.get(breadcrumb, {}).get(k)
