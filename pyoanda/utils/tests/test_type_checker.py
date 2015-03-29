try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from ..type_checker import type_checker

class TypeCheckerTest(unittest.TestCase):
    def test_simple_pass(self):
        item = {"x": 1, "y": None}
        checker = {
            "x": (int, range(1, 10)),
            "y" : (NoneType,)
        }
        type_checker(item, checker)

    def test_simple_fail_type(self):
        item = {"x": "X"}
        checker = { "x": (int, range(1, 10))}
        with self.assertRaises(TypeError):
            type_checker(item, checker)

    def test_simple_fail_range(self):
        item = {"x": 11}
        checker = { "x": (int, range(1, 10))}
        with self.assertRaises(TypeError):
            type_checker(item, checker)

    def test_simple_fail_extra_field(self):
        item = {"x": 1, "y": None}
        checker = { "x": (int, range(1, 10))}
        with self.assertRaises(TypeError):
            type_checker(item, checker)