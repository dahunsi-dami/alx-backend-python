#!/usr/bin/env python3
"""Unittests for client.py module."""
import unittest
from unittest.mock import patch, PropertyMock
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

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test to ensure _public_repos_url fetches repos_url properly.

        Args:
            mock_org: the mocked org property.
        """
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(
            result,
            "https://api.github.com/orgs/testorg/repos"
        )
        mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test to ensure public_repos method returns-
        -the correct list of repos.

        Args:
            mock_get_json: the mocked get_json function.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        expected_repos = ["repo1", "repo2", "repo3"]

        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/testorg/repos"
            )

            client = GithubOrgClient("testorg")
            repos = client.public_repos

            self.assertEqual(repos, expected_repos)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )
