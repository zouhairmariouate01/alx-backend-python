#!/usr/bin/env python3
"""
    Module contains test function that tests utils.py
"""
import unittest
import requests
from unittest.mock import patch, Mock
from parameterized import parameterized
access_nested_map = __import__('utils').access_nested_map
get_json = __import__('utils').get_json
memoize = __import__('utils').memoize


class TestAccessNestedMap(unittest.TestCase):
    """
        Class TestAccessNestedMap inherits from unittest
        to test the functions of utils.py file
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
            Method that test the nested_map function
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
            Method that tests access_nested_map exception
        """
        with self.assertRaises(KeyError) as ar:
            access_nested_map(nested_map, path)
        self.assertEqual(str(ar.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """
        TestGetJson class that inherits from unittest.TestCase
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
            Method that tests that utils.get_json returns the expected result.
        """
        mock_json = Mock(return_value=test_payload)
        mock_get.return_value = Mock(json=mock_json)
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
        return mock_get


class TestMemoize(unittest.TestCase):
    """
        class TestMemoize that inherits from unittest.TestCase
        contains methods to test the memoize function in utils Module
    """

    def test_memoize(self):
        """
            Method that tests memoize function from utils Module
        """
        class TestClass:
            """
                class TestClass
            """
            def a_method(self):
                """
                    Method that returns 42 always
                """
                return 42

            @memoize
            def a_property(self):
                """
                    Method that memoize the a_method and returns its result
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_me:
            testClass = TestClass()
            assert testClass.a_property == testClass.a_property
        mock_me.assert_called_once()
