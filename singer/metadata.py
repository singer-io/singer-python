def new():
    return {}

def to_map(raw_metadata):
    return {tuple(md['breadcrumb']): md['metadata'] for md in raw_metadata}

def to_list(compiled_metadata):
    return [{'breadcrumb': k, 'metadata': v} for k, v in compiled_metadata.items()]

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
