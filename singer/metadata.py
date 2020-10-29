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

def get_properties_metadata(schema, key_properties, parent=()):
    mdata = {}
    if 'object' in schema['type']:
        for field_name, field_props in schema['properties'].items():
            breadcrumb = parent + ('properties', field_name)
            if key_properties and field_name in key_properties:
                inclusion = 'automatic'
            else:
                inclusion = 'available'


            mdata = write(mdata, breadcrumb, 'inclusion', inclusion)
            mdata.update(
                get_properties_metadata(
                    field_props,
                    key_properties,
                    parent=breadcrumb
                )
            )
    elif 'array' in schema['type']:
        breadcrumb = parent + ('items',)
        mdata.update(
            get_properties_metadata(
                schema['items'],
                key_properties,
                parent=breadcrumb
            )
        )

    return mdata

def get_standard_metadata(schema=None, schema_name=None, key_properties=None,
                          valid_replication_keys=None, replication_method=None):
    mdata = {(): {}}

    if key_properties is not None:
        mdata = write(mdata, (), 'table-key-properties', key_properties)
    if replication_method:
        mdata = write(mdata, (), 'forced-replication-method', replication_method)
    if valid_replication_keys is not None:
        mdata = write(mdata, (), 'valid-replication-keys', valid_replication_keys)
    if schema:
        mdata = write(mdata, (), 'inclusion', 'available')

        if schema_name:
            mdata = write(mdata, (), 'schema-name', schema_name)
        mdata.update(get_properties_metadata(schema, key_properties))

    return to_list(mdata)
