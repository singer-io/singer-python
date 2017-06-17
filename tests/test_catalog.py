import unittest

from singer.schema import Schema
from singer.catalog import Catalog, CatalogEntry

class TestCatalog(unittest.TestCase):

    dict_form = {
        'streams': [
            {
                'stream': 'users',
                'tap_stream_id': 'prod_users',
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
            database='prod',
            table='users',
            schema=Schema(
                type='object',
                selected=True,
                properties={
                    'id': Schema(type='integer', selected=True),
                    'name': Schema(type='string', selected=True)})),
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

    def test_from_dict(self):
        self.assertEqual(self.obj_form, Catalog.from_dict(self.dict_form))

    def test_to_dict(self):
        self.assertEqual(self.dict_form, self.obj_form.to_dict())
        
            
