import unittest
from singer.metadata import get_standard_metadata

class TestStandardMetadata(unittest.TestCase):

    def test_standard_metadata_1000(self):

        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                },
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
            },
        ]

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

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=None,
                replication_method=None,
                valid_replication_keys=None
            ),
            expected_metadata)


    def test_standard_metadata_1001(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'valid-replication-keys': ['id','created']
                },
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
            },
        ]

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

        test_rk = ['id', 'created']

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=None,
                replication_method=None,
                valid_replication_keys=test_rk
            ),
            expected_metadata)


    def test_standard_metadata_1010(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'forced-replication-method': 'INCREMENTAL'
                },
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
            },
        ]

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

        test_rm = 'INCREMENTAL'

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=None,
                replication_method=test_rm,
                valid_replication_keys=None
            ),
            expected_metadata)


    def test_standard_metadata_1011(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'valid-replication-keys': ['id','created'],
                    'forced-replication-method': 'INCREMENTAL'
                },
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
            },
        ]

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

        test_rk = ['id', 'created']

        test_rm = 'INCREMENTAL'

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=None,
                replication_method=test_rm,
                valid_replication_keys=test_rk
            ),
            expected_metadata)


    def test_standard_metadata_1100(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'table-key-properties': ['id']
                },
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
            },
        ]

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

        test_kp = ['id']

        test_rk = ['id', 'created']

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=test_kp,
                replication_method=None,
                valid_replication_keys=None
            ),
            expected_metadata)


    def test_standard_metadata_1101(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'table-key-properties': ['id'],
                    'valid-replication-keys': ['id','created']
                },
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
            },
        ]

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

        test_kp = ['id']

        test_rk = ['id','created']

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=test_kp,
                replication_method=None,
                valid_replication_keys=test_rk
            ),
            expected_metadata)


    def test_standard_metadata_1110(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'table-key-properties': ['id'],
                    'forced-replication-method': 'INCREMENTAL'
                },
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
            },
        ]

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

        test_kp = ['id']

        test_rm = 'INCREMENTAL'

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=test_kp,
                replication_method=test_rm,
                valid_replication_keys=None
            ),
            expected_metadata)


    def test_standard_metadata_1111(self):
        expected_metadata = [
            {
                'metadata': {
                    'inclusion': 'available',
                    'table-key-properties': ['id'],
                    'forced-replication-method': 'INCREMENTAL'
                    'valid-replication-keys': ['id','created']
                },
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
            },
        ]

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

        test_kp = ['id']

        test_rm = 'INCREMENTAL'

        test_rk = ['id', 'created']

        self.assertEqual(
            get_standard_metadata(
                schema=test_schema,
                key_properties=test_kp,
                replication_method=test_rm,
                valid_replication_keys=test_rk
            ),
            expected_metadata)


    def test_standard_metadata_no_schemas(self):

        # Some contants shared by a number of expected metadata objects
        test_kp = ['id']
        test_rm = 'INCREMENTAL'
        test_rk = ['id', 'created']

        # test_variables is a list of tuples, where the first element is a
        # dictionary of parameters for `get_standard_metadata()` and the
        # second element is the expected metadata
        test_variables = [
            (
                {
                    schema: None,
                    key_properties: None,
                    replication_method: None,
                    valid_replication_keys: None
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
                    schema: None,
                    key_properties: None,
                    replication_method: None,
                    valid_replication_keys: test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    schema: None,
                    key_properties: None,
                    replication_method: test_rm,
                    valid_replication_keys: None
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
                    schema: None,
                    key_properties: None,
                    replication_method: test_rm,
                    valid_replication_keys: test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'forced-replication-method': 'INCREMENTAL',
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    schema: None,
                    key_properties: test_kp,
                    replication_method: None,
                    valid_replication_keys: None
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
                    schema: None,
                    key_properties: test_kp,
                    replication_method: None,
                    valid_replication_keys: test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'table-key-properties': ['id'],
                            'valid-replication-keys': ['id','created']
                        },
                        'breadcrumb': []
                    }
                ]
            ),
            (
                {
                    metadata: None,
                    key_properties: test_kp,
                    replication_method: test_rm,
                    valid_replication_keys: test_rk
                },
                [
                    {
                        'metadata': {
                            'inclusion': 'available',
                            'table-key-properties': ['id'],
                            'forced-replication-method': 'INCREMENTAL'
                            'valid-replication-keys': ['id','created']
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
