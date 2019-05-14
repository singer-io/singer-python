import unittest
from singer.metadata import get_standard_metadata

def make_expected_metadata(stream_name, base_obj, dict_of_extras):
    metadata_value = {**base_obj}
    metadata_value.update(dict_of_extras)

    return [
        {
            'metadata': metadata_value,
            'schema_name': stream_name,
            'breadcrumb': []
        },
        {
            'metadata': {
                'inclusion': 'available',
            },
            'breadcrumb': ['properties', 'id']
        },
        {
            'metadata': {
                'inclusion': 'available',
            },
            'breadcrumb': ['properties', 'name']
        },
        {
            'metadata': {
                'inclusion': 'available',
            },
            'breadcrumb': ['properties', 'created']
        }
    ]

class TestStandardMetadata(unittest.TestCase):

    def test_standard_metadata(self):

        # Some contants shared by a number of expected metadata objects
        tap_stream_id = 'employees'
        test_kp = ['id']
        test_rm = 'INCREMENTAL'
        test_rk = ['id', 'created']
        metadata_kp = {'table-key-properties': ['id']}
        metadata_rm = {'forced-replication-method': 'INCREMENTAL'}
        metadata_rk = {'valid_replication_keys': ['id','created']}
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
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'valid_replication_keys': ['id','created']}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'forced-replication-method': 'INCREMENTAL'}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'valid_replication_keys': ['id','created'],
                    'forced-replication-method': 'INCREMENTAL'}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'table-key-properties': ['id']}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                    'valid_replication_keys': ['id','created']}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                    'forced-replication-method': 'INCREMENTAL'}
                )
            ),
            (
                {
                    'schema': test_schema,
                    'schema_name': tap_stream_id,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                make_expected_metadata(
                    tap_stream_id,
                    schema_present_base_obj,
                    {'table-key-properties': ['id'],
                     'forced-replication-method': 'INCREMENTAL',
                     'valid_replication_keys': ['id','created']}
                )
            ),
            (
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {},
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'valid_replication_keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'forced-replication-method': 'INCREMENTAL'
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': None,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'forced-replication-method': 'INCREMENTAL',
                            'valid_replication_keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': None
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'table-key-properties': ['id'],
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': None,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'table-key-properties': ['id'],
                            'valid_replication_keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    'schema': None,
                    'key_properties': test_kp,
                    'replication_method': test_rm,
                    'valid_replication_keys': test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'table-key-properties': ['id'],
                            'forced-replication-method': 'INCREMENTAL',
                            'valid_replication_keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            )
        ]

        for var in test_variables:
            function_params = var[0]
            expected_metadata = var[1]
            self.assertEqual(get_standard_metadata(**function_params),
                             expected_metadata)
