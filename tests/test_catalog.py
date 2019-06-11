import unittest
import singer.catalog 

from singer.schema import Schema
from singer.catalog import Catalog, CatalogEntry

dict_form = {
        'streams': [
            {
                'stream': 'users',
                'tap_stream_id': 'prod_users',
                'stream_alias': 'users_alias',
                'database_name': 'prod',
                'table_name': 'users',
                'schema': {
                    'type': 'object',
                    'selected': True,
                    'properties': {
                        'id': {'type': 'integer', 'selected': True},
                        'name': {'type': 'string', 'selected': True}
                    }
                },
                'metadata': [
                    {
                        'metadata': {
                            'metadata-key': 'metadata-value'
                        },
                        'breadcrumb': [
                            'properties',
                            'name',
                        ],
                    },
                ],
            },
            {
                'stream': 'orders',
                'tap_stream_id': 'prod_orders',
                'database_name': 'prod',
                'table_name': 'orders',
                'schema': {
                    'type': 'object',
                    'selected': True,
                    'properties': {
                        'id': {'type': 'integer', 'selected': True},
                        'amount': {'type': 'number', 'selected': True}
                        }
                    }
                }
            ]
        }

obj_form = Catalog(streams=[
        CatalogEntry(
            stream='users',
            tap_stream_id='prod_users',
            stream_alias='users_alias',
            database='prod',
            table='users',
            schema=Schema(
                type='object',
                selected=True,
                properties={
                    'id': Schema(type='integer', selected=True),
                    'name': Schema(type='string', selected=True)}),
            metadata=[{
                'metadata': {
                    'metadata-key': 'metadata-value'
                },
                'breadcrumb': [
                    'properties',
                    'name',
                ],
            }]),
        CatalogEntry(
            stream='orders',
            tap_stream_id='prod_orders',
            database='prod',
            table='orders',
            schema=Schema(
                type='object',
                selected=True,
                properties={
                    'id': Schema(type='integer', selected=True),
                    'amount': Schema(type='number', selected=True)}))])




class TestToDictAndFromDict(unittest.TestCase):
    def test_from_dict(self):
        self.assertEqual(obj_form, Catalog.from_dict(dict_form))

    def test_to_dict(self):
        self.assertEqual(dict_form, obj_form.to_dict())
        

class TestGetStream(unittest.TestCase):
    def test(self):
        catalog = Catalog(
            [CatalogEntry(tap_stream_id='a'),
             CatalogEntry(tap_stream_id='b'),
             CatalogEntry(tap_stream_id='c')])
        entry = catalog.get_stream('b')
        self.assertEquals('b', entry.tap_stream_id)

class TestWriteCatalog(unittest.TestCase):
    def test(self):
        singer.catalog.write_catalog(dict_form)
