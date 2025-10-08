import unittest
from singer.schema_generation import generate_schema

class TestSchemaGeneration(unittest.TestCase):
    def test_simple_schema(self):
        records = [{'a': 1, 'b': 'two', 'c': True, 'dt': '2000-01-01T00:11:22Z'}]
        expected_schema = {
            'type': ['null', 'object'],
            'properties': {
                'a': {'type': ['null', 'integer']},
                'b': {'type': ['null', 'string']},
                'c': {'type': ['null', 'boolean']},
                'dt': {'type': ['null', 'string']}
            }
        }
        self.assertEqual(expected_schema, generate_schema(records))

    def test_mix_n_match_records_schema(self):
        records = [
            {'a': 1, 'b': 'b'},
            {'a': 'two', 'c': 7, 'd': [1, 'two']},
            {'a': True, 'c': 7.7, 'd': {'one': 1, 'two': 'two'}}
        ]
        expected_schema = {
            'type': ['null', 'object'],
            'properties': {'a': {'anyOf': [{'type': ['null', 'integer']},
                                           {'type': ['null', 'boolean']},
                                           {'type': ['null', 'string']}]},
                           'b': {'type': ['null', 'string']},
                           'c': {'anyOf': [{'type': ['null', 'string'], 'format': 'singer.decimal'},
                                           {'type': ['null', 'integer']}]},
                'd': {'anyOf': [{'type': ['null', 'array'],
                                 'items': {'anyOf': [{'type': ['null', 'integer']},
                                                     {'type': ['null', 'string']}]}},
                                {'type': ['null', 'object'],
                                 'properties': {'one': {'type': ['null', 'integer']},
                                                'two': {'type': ['null', 'string']}}}]}}
        }
        actual_schema = generate_schema(records)
        self.assertEqual(expected_schema, actual_schema)

    def test_nested_structue_schema(self):
        records = [{'a': {'b': {'c': [{'d': 7}]}, 'e': [[1, 2, 3]]}}]
        expected_schema = {
            'type': ['null', 'object'],
            'properties': {
                'a': {
                    'type': ['null', 'object'],
                    'properties': {
                        'b': {
                            'type': ['null', 'object'],
                            'properties': {
                                'c': {
                                    'type': ['null', 'array'],
                                    'items': {
                                        'type': ['null', 'object'],
                                        'properties': {'d': {'type': ['null', 'integer']}}
                                    }
                                }
                            }
                        },
                        'e': {
                            'type': ['null', 'array'],
                            'items': {
                                'type': ['null', 'array'],
                                'items': {'type': ['null', 'integer']}}
                        }
                    }
                }
            }
        }
        self.assertEqual(expected_schema, generate_schema(records))
