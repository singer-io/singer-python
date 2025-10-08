def add_observation(acc, path):

    node = acc
    for i in range(0, len(path) - 1):
        k = path[i]
        if k not in node:
            node[k] = {}
        node = node[k]

    node[path[-1]] = True

# pylint: disable=too-many-branches
def add_observations(acc, path, data):
    if isinstance(data, dict):
        for key in data:
            add_observations(acc, path + ["object", key], data[key])
    elif isinstance(data, list):
        if len(data) == 0:
            add_observations(acc, path + ["array"], None)
        for item in data:
            add_observations(acc, path + ["array"], item)
    elif isinstance(data, str):
        try:
            # If the string parses as a int, add an observation that it's a integer
            int(data)
            add_observation(acc, path + ["integer"])
            return acc
        except (ValueError, TypeError):
            pass
        try:
            # If the string parses as a float, add an observation that it's a number
            float(data)
            add_observation(acc, path + ["number"])
            return acc
        except (ValueError, TypeError):
            pass
        add_observation(acc, path + ["string"])
    elif isinstance(data, bool):
        add_observation(acc, path + ["boolean"])
    elif isinstance(data, int):
        add_observation(acc, path + ["integer"])
    elif isinstance(data, float):
        add_observation(acc, path + ["number"])
    elif data is None:
        add_observation(acc, path + ["null"])
    else:
        raise Exception("Unexpected value " + repr(data) + " at path " + repr(path))

    return acc

def to_json_schema(obs):
    types = []
    # add schema types in a specific order to anyOf list
    for key in ['array', 'object', 'number', 'integer', 'boolean', 'string', 'null']:
        if key not in obs:
            continue

        result = {'type': ['null']}

        if key == 'object':
            result['type'] += ['object']
            if 'properties' not in result:
                result['properties'] = {}
                for obj_key in obs['object']:
                    result['properties'][obj_key] = to_json_schema(obs['object'][obj_key])

        elif key == 'array':
            result['type'] += ['array']
            result['items'] = to_json_schema(obs['array'])

        elif key == 'string':
            result['type'] += ['string']

        elif key == 'boolean':
            result['type'] += ['boolean']

        elif key == 'integer':
            result['type'] += ['integer']

        elif key == 'number':
            # Use type=string, format=singer.decimal
            result['type'] += ['string']
            result['format'] = 'singer.decimal'

        elif key == 'null':
            pass

        else:
            raise Exception("Unexpected data type " + key)

        types.append(result)

    if len(types) == 0:
        return {'type': ['null', 'string']}

    if len(types) == 1:
        return types[0]

    return {'anyOf': types}

def generate_schema(records):
    obs = {}
    for record in records:
        obs = add_observations(obs, [], record)
    return to_json_schema(obs)
