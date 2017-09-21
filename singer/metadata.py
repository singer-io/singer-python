def compile_metadata(catalog):
    md_dict = {}
    for mdata in catalog.get('metadata'):
        breadcrumb = tuple(mdata['breadcrumb'])
        if md_dict.get(breadcrumb) is None:
            md_dict[breadcrumb] = mdata.get('metadata')
        else:
            md_dict[breadcrumb].update(mdata.get('metadata'))

    return md_dict
