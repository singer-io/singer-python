from pprint import pprint
import unittest
from singer.metadata import get_standard_metadata, to_map

def make_expected_metadata(base_obj, dict_of_extras, has_pk=False):
    metadata_value = {**base_obj}
    metadata_value.update(dict_of_extras)

    return [
        {
            'metadata': metadata_value,
            'breadcrumb': ()
        },
        {
            'metadata': {
                'inclusion': 'automatic' if has_pk else 'available',
            },
            'breadcrumb': ('properties', 'id')
        },
        {
            'metadata': {
                'inclusion': 'available',
            },
            'breadcrumb': ('properties', 'name')
        },
        {
            'metadata': {
                'inclusion': 'available',
            },
            'breadcrumb': ('properties', 'created')
        }
    ]

class TestStandardMetadata(unittest.TestCase):

    def test_standard_metadata(self):
        """
        There's four inputs we want to test: schema, key_properties, replication_method, valid_replication_keys.

        When `schema` is a non-null input, we expect `"inclusion": "available"` metadata for the `()` breadcrumb.

        When `key_properties` is a non-null input, we expect `table-key-properties` metadata for the `()` breadcrumb.

        When `replication_method` is a non-null input, we expect `forced-replication-method` metadata for the `()` breadcrumb.

        When `valid_replication_keys` is a non-null input, we expect `valid-replication-keys` metadata for the `()` breadcrumb.
        """
        self.maxDiff = None

        # Some contants shared by a number of expected metadata objects
        tap_stream_id = 'employees'
        test_kp = ['id']
        test_rm = 'INCREMENTAL'
        test_rk = ['id', 'created']
        metadata_kp = {'table-key-properties': ['id']}
        metadata_rm = {'forced-replication-method': 'INCREMENTAL'}
        metadata_rk = {'valid-replication-keys': ['id','created']}
        schema_present_base_obj = {'inclusion': 'available'}
        test_schema = {
            'type': ['null', 'object'],
            'additionalProperties': False,
            'properties': {
                'id': {'type': ['null', 'string']},
                'name': {'type': ['null', 'string']},
                'created': {'type': ['null', 'string'],
                            'format': 'date-time'},
            }
        }

        # test_variables is a list of tuples, where the first element is a
        # dictionary of parameters for `get_standard_metadata()` and the
        # second element is the expected metadata
        test_variables = [
            ( # test_number=0
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'schema-name': tap_stream_id,}
                )
            ),
            ( # test_number=1
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'valid-replication-keys': ['id','created'],
                     'schema-name':tap_stream_id}
                )
            ),
            ( # test_number=2
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'forced-replication-method': 'INCREMENTAL',
                     'schema-name':tap_stream_id}
                )
            ),
            ( # test_number=3
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'valid-replication-keys': ['id','created'],
                     'forced-replication-method': 'INCREMENTAL',
                     'schema-name':tap_stream_id}
                )
            ),
            ( # test_number=4
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                     'schema-name':tap_stream_id},
                    has_pk=True
                )
            ),
            ( # test_number=5
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                     'valid-replication-keys': ['id','created'],
                     'schema-name':tap_stream_id},
                    has_pk=True
                )
            ),
            ( # test_number=6
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                     'forced-replication-method': 'INCREMENTAL',
                     'schema-name':tap_stream_id},
                    has_pk=True
                )
            ),
            ( # test_number=7
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                     'forced-replication-method': 'INCREMENTAL',
                     'valid-replication-keys': ['id','created'],
                     'schema-name':tap_stream_id},
                    has_pk=True
                )
            ),
            ( # test_number=8
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                []
            ),
            ( # test_number=9
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=10
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {
                            'forced-replication-method': 'INCREMENTAL'
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=11
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'forced-replication-method': 'INCREMENTAL',
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=12
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {
                            'table-key-properties': ['id'],
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=13
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'table-key-properties': ['id'],
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=14
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {
                            'table-key-properties': ['id'],
                            'forced-replication-method': 'INCREMENTAL',
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            ( # test_number=15
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'table-key-properties': ['id'],
                            'forced-replication-method': 'INCREMENTAL',
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            )
        ]

        for i, var in enumerate(test_variables):
            with self.subTest(test_number=i):
                function_params = var[0]
                expected_metadata = var[1]

                test_value = get_standard_metadata(**function_params)

                expected_value = to_map(expected_metadata)
                actual_value = to_map(test_value)
                self.assertDictEqual(expected_value, actual_value)

        # Test one function call where the parameters are not splat in
        test_value = get_standard_metadata(test_schema,
                                           tap_stream_id,
                                           test_kp,
                                           test_rk,
                                           test_rm)

        expected_metadata = make_expected_metadata(schema_present_base_obj,
                                                   {'table-key-properties': ['id'],
                                                    'forced-replication-method': 'INCREMENTAL',
                                                    'valid-replication-keys': ['id','created'],
                                                    'schema-name':tap_stream_id},
                                                   has_pk=True)
        self.assertDictEqual(
            to_map(expected_metadata),
            to_map(test_value)
        )

    def test_empty_key_properties_are_written(self):
        mdata = get_standard_metadata(key_properties=[])
        self.assertEqual(mdata, [{'breadcrumb': (), 'metadata': {'table-key-properties': []}}])

    def test_empty_valid_replication_keys_are_written(self):
        mdata = get_standard_metadata(valid_replication_keys=[])
        self.assertEqual(mdata, [{'breadcrumb': (), 'metadata': {'valid-replication-keys': []}}])
