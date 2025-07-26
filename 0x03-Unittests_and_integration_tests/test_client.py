#!/usr/bin/env python3
"""Test module for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
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
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_pub_repos_url, \
                patch('client.GithubOrgClient.get_json') as mock_get_json, \
                patch('client.GithubOrgClient.public_repos',
                      return_value=[repo['name'] for repo in self.repos_payload]):

            mock_pub_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos")
            mock_get_json.return_value = self.repos_payload

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected_repos = [repo['name'] for repo in self.repos_payload]
            self.assertEqual(result, expected_repos)
            mock_pub_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter"""
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_pub_repos_url, \
                patch('client.GithubOrgClient.get_json') as mock_get_json, \
                patch('client.GithubOrgClient.public_repos',
                      return_value=[repo['name'] for repo in self.apache_repos]):

            mock_pub_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos")
            mock_get_json.return_value = self.repos_payload

            client = GithubOrgClient("google")
            result = client.public_repos(license="apache-2.0")

            expected_repos = [repo['name'] for repo in self.apache_repos]
            self.assertEqual(result, expected_repos)
            mock_pub_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")


if __name__ == '__main__':
    unittest.main()
