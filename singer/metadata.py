def compile_metadata(catalog):
    md_dict = {}
    for md in catalog.get('metadata'):
        breadcrumb = tuple(md['breadcrumb'])
        if md_dict.get(breadcrumb) is None:
            md_dict[breadcrumb] = md.get('metadata')
        else:
            md_dict[breadcrumb].update(md.get('metadata'))

    return md_dict
