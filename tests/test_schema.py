import unittest

from singer.schema import Schema

class TestSchema(unittest.TestCase):

    dict_form = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
                'maxLength': 32
            },
            'name': {
                'type': 'string'
            },
            'birth_date': {
                'type': 'string',
                'format': 'date-time'
            }
        }
    }

    obj_form = Schema(
        type='object',
        properties={
            'id': Schema(type='string', maxLength=32),
            'name': Schema(type='string'),
            'birth_date': Schema(type='string', format='date-time')})

    def test_to_dict(self):
        self.assertEquals(self.dict_form, self.obj_form.to_dict())

    def test_from_dict(self):
        self.assertEquals(self.obj_form, Schema.from_dict(self.dict_form))
                
    
