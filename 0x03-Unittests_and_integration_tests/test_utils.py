#!/usr/bin/env python3
"""Unittests for utils.py."""

import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for access_nested_map function to-
    -return what is should return.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, error):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{error}'")


class TestGetJson(unittest.TestCase):
    """
    Tests for get_json function to return-
    -what it should return.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    # Patch (replace) requests.get method with utils module
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # Use mock object to mimic behavior of real HTTP response.
        mock_response = Mock()

        # Make mock_response return test_payload to-
        # -simulate JSON resopnse by real HTTP request.
        mock_response.json.return_value = test_payload

        # Setting patched requests.get to-
        # -return mock_response when called.
        mock_get.return_value = mock_response

        json_response = get_json(test_url)

        # Test mocked get() was called only once per input-
        # -w/ test_url as argument.
        mock_get.assert_called_once_with(test_url)

        self.assertEqual(json_response, test_payload)


class TestMemoize(unittest.TestCase):
    """Class with a test_memoize method."""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        TC_instance = TestClass()

        with patch.object(TestClass, 'a_method', return_value=42) \
                as mock_method:
            result1 = TC_instance.a_property
            result2 = TC_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
