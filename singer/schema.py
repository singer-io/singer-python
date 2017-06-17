# pylint: disable=redefined-builtin, too-many-arguments, invalid-name
'''Provides an object model for JSON Schema'''

import json

# These are standard keys defined in the JSON Schema spec
STANDARD_KEYS = [
    'sqlDatatype',
    'selected',
    'inclusion',
    'description',
    'minimum',
    'maximum',
    'exclusiveMinimum',
    'exclusiveMaximum',
    'multipleOf',
    'maxLength',
    'format',
    'type'
]


class Schema(object):  # pylint: disable=too-many-instance-attributes
    '''Object model for JSON Schema.

    Tap and Target authors may find this to be more convenient than
    working directly with JSON Schema data structures.

    '''

    def __init__(self, type=None, format=None, properties=None,
                 items=None, sqlDatatype=None, selected=None,
                 inclusion=None, description=None, minimum=None,
                 maximum=None, exclusiveMinimum=None,
                 exclusiveMaximum=None, multipleOf=None, maxLength=None):

        self.type = type
        self.properties = properties
        self.items = items
        self.sqlDatatype = sqlDatatype
        self.selected = selected
        self.inclusion = inclusion
        self.description = description
        self.minimum = minimum
        self.maximum = maximum
        self.exclusiveMinimum = exclusiveMinimum
        self.exclusiveMaximum = exclusiveMaximum
        self.multipleOf = multipleOf
        self.maxLength = maxLength
        self.format = format

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_dict(self):
        '''Return the raw JSON Schema as a (possibly nested) dict.'''
        result = {}
        if self.properties:
            result['properties'] = {
                k: v.to_dict()
                for k, v
                in self.properties.items()  # pylint: disable=no-member
            }
        if self.items:
            result['items'] = self.items.to_dict()  # pylint: disable=no-member
        for key in STANDARD_KEYS:
            if self.__dict__[key] is not None:
                result[key] = self.__dict__[key]

        return result

    @classmethod
    def from_dict(cls, data):
        '''Initialize a Schema object based on the JSON Schema structure.'''
        kwargs = {}
        properties = data.get('properties')
        items = data.get('items')

        if properties:
            kwargs['properties'] = {
                k: Schema.from_dict(v) for k, v in properties.items()
            }
        if items:
            kwargs['items'] = Schema.from_dict(items)
        for key in STANDARD_KEYS:
            if key in data:
                kwargs[key] = data[key]
        return Schema(**kwargs)
