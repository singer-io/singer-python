import unittest

from singer.schema import Schema

class TestSchema(unittest.TestCase):

    # Raw data structures for several schema types
    string_dict = {
        'type': 'string',
        'maxLength': 32
    }

    integer_dict = {
        'type': 'integer',
        'maximum': 1000000
    }

    array_dict = {
        'type': 'array',
        'items': integer_dict
    }

    object_dict = {
        'type': 'object',
        'properties': {
            'a_string': string_dict,
            'an_array': array_dict
        }
    }

    # Schema object forms of the same schemas as above
    string_obj = Schema(type='string', maxLength=32)

    integer_obj = Schema(type='integer', maximum=1000000)

    array_obj = Schema(type='array', items=integer_obj)

    object_obj = Schema(type='object',
                        properties={'a_string': string_obj,
                                    'an_array': array_obj})

    def test_string_to_dict(self):
        self.assertEquals(self.string_dict, self.string_obj.to_dict())

    def test_integer_to_dict(self):
        self.assertEquals(self.integer_dict, self.integer_obj.to_dict())

    def test_array_to_dict(self):
        self.assertEquals(self.array_dict, self.array_obj.to_dict())

    def test_object_to_dict(self):
        self.assertEquals(self.object_dict, self.object_obj.to_dict())        

    def test_string_from_dict(self):
        self.assertEquals(self.string_obj, Schema.from_dict(self.string_dict))

    def test_integer_from_dict(self):
        self.assertEquals(self.integer_obj, Schema.from_dict(self.integer_dict))

    def test_array_from_dict(self):        
        self.assertEquals(self.array_obj, Schema.from_dict(self.array_dict))

    def test_object_from_dict(self):        
        self.assertEquals(self.object_obj, Schema.from_dict(self.object_dict))        
                
    
