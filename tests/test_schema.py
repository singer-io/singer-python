import unittest

from singer.schema import Schema

class TestSchema(unittest.TestCase):

    def test_constructor(self):
        schema = Schema(
            type='object',
            properties={
                'id': Schema(type='string', maxLength=32),
                'name': Schema(type='string'),
                'birth_date': Schema(type='string', format='date-time')})
        self.assertEquals(
            {'type': 'object',
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
            },
            schema.to_dict())              
                
