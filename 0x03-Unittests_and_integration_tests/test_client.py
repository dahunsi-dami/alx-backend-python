#!/usr/bin/env python3
"""Unittests for client.py module."""
import unittest
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests to ensure method in GithubOrgClient class-
    -give expected outputs.
    """
    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google"),
        ("abc", "https://api.github.com/orgs/abc")
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_url, mock_get_json):
        """
        Test to ensure GithubOrgClient methods give correct output.

        Args:
            org_name: name of the GitHub org.
            expected_url: URL to call get_json with.
            mock_get_json: the mocked get_json function.
        """
        client = GithubOrgClient(org_name)

        mock_get_json.return_value = {
            "repos_url": "https://api.github.com/orgs/{org}/repos"
        }

        response = client.org

        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(response, mock_get_json.return_value)
