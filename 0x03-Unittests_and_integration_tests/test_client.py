#!/usr/bin/env python3
"""Unittests for client.py module."""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from typing import Dict
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
from requests import HTTPError


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
        """
        with patch(
            "client.get_json",
            return_value=[{
                "name": "repo1"},
                {"name": "repo2"},
                {"name": "repo3"}
            ]
        ) as mock_get_json:

            with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock
            ) as mock_public_repos_url:
                mock_public_repos_url.return_value = (
                    "https://api.github.com/orgs/testorg/repos"
                )

                client = GithubOrgClient("testorg")
                repos = client.public_repos()

                expected_repos = ["repo1", "repo2", "repo3"]

                self.assertEqual(repos, expected_repos)

                mock_public_repos_url.assert_called_once()
                mock_get_json.assert_called_once_with(
                    "https://api.github.com/orgs/testorg/repos"
                )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test ensures `has_license` method returns correct boolean-
        -when checked if repo has the specified license.

        Args:
            repo: dict containing repo data, including license.
            license_key: key of license to check.
            expected: the expected result as True or False.
        """
        client = GithubOrgClient("testorg")

        result = client.has_license(repo, license_key)

        self.assertEqual(result, expected)

    @parameterized_class([
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos
         }
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """
        Integration test for GithubOrgClient.public_repos method.
        """

        @classmethod
        def setUpClass(cls):
            """
            Set up class-level mock responses for external requests.
            """
            cls.get_patcher = patch('requests.get')
            cls.mock_get = cls.get_patcher.start()

            def get_json_side_effect(url):
                if url == 'https://api.github.com/orgs/testorg':
                    return cls.org_payload
                elif url == 'https://api.github.com/orgs/testorg/repos':
                    return cls.repos_payload
                return None

            cls.mock_get.return_value = MagicMock()
            cls.mock_get.return_value.json.side_effect = get_json_side_effect

        @classmethod
        def tearDownClass(cls):
            """Stop the patcher after all the tests."""
            cls.get_patcher.stop()

        def test_public_repos(self):
            """Tests the public_repos method."""
            client = GithubOrgClient("testorg")
            self.assertEqual(client.public_repos(), self.expected_repos)
