import json
import attr

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

@attr.s # pylint: disable=too-many-instance-attributes
class Schema(object):
    '''Object model for JSON Schema.

    Tap and Target authors may find this to be more convenient than
    working directly with JSON Schema data structures.

    '''

    type = attr.ib(default=None)
    properties = attr.ib(default={})
    items = attr.ib(default={})
    sqlDatatype = attr.ib(default=None)
    selected = attr.ib(default=None)
    inclusion = attr.ib(default=None)
    description = attr.ib(default=None)
    minimum = attr.ib(default=None)
    maximum = attr.ib(default=None)
    exclusiveMinimum = attr.ib(default=None)
    exclusiveMaximum = attr.ib(default=None)
    multipleOf = attr.ib(default=None)
    maxLength = attr.ib(default=None)
    format = attr.ib(default=None)

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        '''Return the raw JSON Schema as a (possibly nested) dict.'''
        result = {}
        if self.properties:
            result['properties'] = {
                k: v.to_dict() for k, v in self.properties.items() # pylint: disable=no-member
            }
        if self.items:
            result['items'] = self.items.to_dict()
        for key in STANDARD_KEYS:
            if self.__dict__[key] is not None:
                result[key] = self.__dict__[key]

        return result

    @classmethod
    def from_dict(self, data):
        '''Initialize a Schema object based on the raw JSON Schema data structure.'''
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

