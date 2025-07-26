#!/usr/bin/env python3
"""Test module for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""
        cls.org_payload = TEST_PAYLOAD[0][0]
        cls.repos_payload = TEST_PAYLOAD[0][1]
        cls.apache_repos = TEST_PAYLOAD[0][2]

    def test_public_repos(self):
        """Test public_repos method without license filter"""
        test_url = "https://api.github.com/orgs/google/repos"
        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock
        ) as mock_repos_url, \
                patch(
                    'client.GithubOrgClient.get_json'
                ) as mock_get, \
                patch(
                    'client.GithubOrgClient.public_repos',
                    return_value=[repo['name'] for repo in self.repos_payload]
                ):

            mock_repos_url.return_value = test_url
            mock_get.return_value = self.repos_payload

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected = [repo['name'] for repo in self.repos_payload]
            self.assertEqual(result, expected)
            mock_repos_url.assert_called_once()
            mock_get.assert_called_once_with(test_url)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter"""
        test_url = "https://api.github.com/orgs/google/repos"
        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock
        ) as mock_repos_url, \
                patch(
                    'client.GithubOrgClient.get_json'
                ) as mock_get, \
                patch(
                    'client.GithubOrgClient.public_repos',
                    return_value=[repo['name'] for repo in self.apache_repos]
                ):

            mock_repos_url.return_value = test_url
            mock_get.return_value = self.repos_payload

            client = GithubOrgClient("google")
            result = client.public_repos(license="apache-2.0")

            expected = [repo['name'] for repo in self.apache_repos]
            self.assertEqual(result, expected)
            mock_repos_url.assert_called_once()
            mock_get.assert_called_once_with(test_url)


if __name__ == '__main__':
    unittest.main()
