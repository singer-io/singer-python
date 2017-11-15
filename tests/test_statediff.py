import unittest
import singer.statediff as statediff

class TestPaths(unittest.TestCase):

    def test_simple_dict(self):

        self.assertEqual(
            [(('a',), 1),
             (('b',), 2)],
            statediff.paths({'a': 1, 'b': 2}))

    def test_nested_dict(self):
        self.assertEqual(
            [(('a', 'b'), 1),
             (('a', 'c'), 2),
             (('d', 'e'), 3)],
            statediff.paths(
                {
                    'a': {
                        'b': 1,
                        'c': 2
                    },
                    'd': {
                        'e': 3
                    }
                }
            )
        )
            

    def test_simple_array(self):
        self.assertEqual(
            [((0,), 'blue'),
             ((1,), 'green')],
            statediff.paths(
                ['blue', 'green']))

    def test_nested_array(self):
        self.assertEqual(
            [((0, 0), 'blue'),
             ((0, 1), 'red'),
             ((1, 0), 'green')],
            statediff.paths([['blue', 'red'], ['green']]))

    def test_arrays_in_dicts(self):
        self.assertEqual(
            [(('a', 0), 'blue'),
             (('a', 1), 'red'),
             (('b', 0), 'green')],
            statediff.paths(
                {
                    'a': ['blue', 'red'],
                    'b': ['green']
                }
            )
        )
                
