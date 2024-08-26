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
        """
        Tests access_nested_map w/ various input parameters.

        Args:
            nested_map: nested map (dict) to access.
            path: structed path to access value in nested map.
            expected: expected value at end of path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, error):
        """
        Tests access_nested_map w/ invalid paths-
        -to get expected KeyError.

        Args:
            nested_map: nested map (dict) to access.
            path: structed path to access value in nested map.
            error: expected error (KeyError).
        """
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
        """
        Tests get_json w/ various URLs and expected payloads.

        Args:
            test_url: URL to get data from.
            test_payload: expected payload from mocked request.
            mock_get: patced `requests.get` mock object.
        """

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
    """
    Tests for memoize function in utils-
    -to make sure it returns what it should.
    """

    def test_memoize(self):
        """
        These tests assert that memoize function is
        a wrapped method called only once and that
        it returns what it should.
        """
        class TestClass:
            """Simple class w/ a method & memoized property."""

            def a_method(self):
                """Simple method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """
                Memoized property method that-
                - returns result of a_method().
                """
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
