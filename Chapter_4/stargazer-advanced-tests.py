import unittest
from unittest.mock import patch, Mock, MagicMock
import json
import requests
from datetime import datetime

# Import the classes we want to test
# Note: You'll need to adjust this import to match your actual file structure
from stargazers_advanced import GitHubAPIClient, GitHubStarsClient

class TestGitHubStarsClient(unittest.TestCase):
    """Test cases for the GitHubStarsClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "https://api.github.com"
        self.api_key = "test_api_key"
        self.client = GitHubStarsClient(self.base_url, self.api_key)
        
        # Common test data
        self.owner = "octocat"
        self.repo = "hello-world"
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_list_repository_stars(self, mock_get):
        """Test listing repository stargazers."""
        # Mock data
        mock_response = [
            {"id": 1, "login": "user1"},
            {"id": 2, "login": "user2"}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.list_repository_stars(self.owner, self.repo, per_page=10, page=1)
        
        # Assertions
        mock_get.assert_called_once_with(
            f"repos/{self.owner}/{self.repo}/stargazers", 
            params={'per_page': 10, 'page': 1}
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.put')
    def test_star_repository(self, mock_put):
        """Test starring a repository."""
        # Call the method
        self.client.star_repository(self.owner, self.repo)
        
        # Assertions
        mock_put.assert_called_once_with(
            f"user/starred/{self.owner}/{self.repo}", 
            data={}
        )
    
    @patch('stargazers_advanced.GitHubAPIClient.delete')
    def test_unstar_repository(self, mock_delete):
        """Test unstarring a repository."""
        # Call the method
        self.client.unstar_repository(self.owner, self.repo)
        
        # Assertions
        mock_delete.assert_called_once_with(
            f"user/starred/{self.owner}/{self.repo}"
        )
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_check_starred_true(self, mock_get):
        """Test checking if a repository is starred (true case)."""
        # Mock response
        mock_get.return_value = {}  # Just needs to not raise an exception
        
        # Call the method
        result = self.client.check_starred(self.owner, self.repo)
        
        # Assertions
        mock_get.assert_called_once_with(f"user/starred/{self.owner}/{self.repo}")
        self.assertTrue(result)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_check_starred_false(self, mock_get):
        """Test checking if a repository is starred (false case)."""
        # Mock response to raise 404
        http_error = requests.exceptions.HTTPError()
        response_mock = Mock()
        response_mock.status_code = 404
        http_error.response = response_mock
        mock_get.side_effect = http_error
        
        # Call the method
        result = self.client.check_starred(self.owner, self.repo)
        
        # Assertions
        mock_get.assert_called_once_with(f"user/starred/{self.owner}/{self.repo}")
        self.assertFalse(result)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_list_starred_repositories_by_other_user(self, mock_get):
        """Test listing repositories starred by another user."""
        # Mock data
        username = "testuser"
        mock_response = [
            {"name": "repo1", "owner": {"login": "user1"}},
            {"name": "repo2", "owner": {"login": "user2"}}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.list_starred_repositories(
            username=username, 
            per_page=5, 
            sort="updated", 
            direction="desc"
        )
        
        # Assertions
        mock_get.assert_called_once_with(
            f"users/{username}/starred", 
            params={'per_page': 5, 'sort': 'updated', 'direction': 'desc'}
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_list_starred_repositories_by_authenticated_user(self, mock_get):
        """Test listing repositories starred by the authenticated user."""
        # Mock data
        mock_response = [
            {"name": "repo1", "owner": {"login": "user1"}},
            {"name": "repo2", "owner": {"login": "user2"}}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.list_starred_repositories(per_page=5)
        
        # Assertions
        mock_get.assert_called_once_with(
            "user/starred", 
            params={'per_page': 5}
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_get_star_count(self, mock_get):
        """Test getting star count for a repository."""
        # Mock data
        mock_response = {
            "id": 123,
            "name": "hello-world",
            "stargazers_count": 42
        }
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_star_count(self.owner, self.repo)
        
        # Assertions
        mock_get.assert_called_once_with(f"repos/{self.owner}/{self.repo}")
        self.assertEqual(result, 42)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_get_star_history_single_page(self, mock_get):
        """Test getting star history with only one page of results."""
        # Mock data
        mock_response = [
            {"user": {"login": "user1"}, "starred_at": "2023-01-01T00:00:00Z"},
            {"user": {"login": "user2"}, "starred_at": "2023-01-02T00:00:00Z"}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_star_history(self.owner, self.repo, per_page=10)
        
        # Assertions
        mock_get.assert_called_once_with(
            f"repos/{self.owner}/{self.repo}/stargazers",
            params={'per_page': 10, 'page': 1},
            headers={"Accept": "application/vnd.github.v3.star+json"}
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_get_star_history_multiple_pages(self, mock_get):
        """Test getting star history with multiple pages of results."""
        # Mock data for first page (full page)
        page1 = [{"user": {"login": f"user{i}"}, "starred_at": f"2023-01-0{i}T00:00:00Z"} for i in range(1, 6)]
        # Mock data for second page (partial page)
        page2 = [{"user": {"login": f"user{i}"}, "starred_at": f"2023-01-0{i}T00:00:00Z"} for i in range(6, 8)]
        
        # Set up the mock to return different values on successive calls
        mock_get.side_effect = [page1, page2]
        
        # Call the method
        result = self.client.get_star_history(self.owner, self.repo, per_page=5)
        
        # Assertions
        expected_calls = [
            unittest.mock.call(
                f"repos/{self.owner}/{self.repo}/stargazers",
                params={'per_page': 5, 'page': 1},
                headers={"Accept": "application/vnd.github.v3.star+json"}
            ),
            unittest.mock.call(
                f"repos/{self.owner}/{self.repo}/stargazers",
                params={'per_page': 5, 'page': 2},
                headers={"Accept": "application/vnd.github.v3.star+json"}
            )
        ]
        mock_get.assert_has_calls(expected_calls)
        self.assertEqual(result, page1 + page2)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_get_trending_repositories(self, mock_get):
        """Test getting trending repositories."""
        # Mock data
        mock_response = [
            {"full_name": "user1/repo1", "stargazers_count": 100},
            {"full_name": "user2/repo2", "stargazers_count": 50}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_trending_repositories(
            language="python", 
            since="weekly", 
            spoken_language="en"
        )
        
        # Assertions
        mock_get.assert_called_once_with(
            "trending/repositories", 
            params={'language': 'python', 'since': 'weekly', 'spoken_language_code': 'en'}
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.get_raw')
    def test_export_stargazers(self, mock_get_raw):
        """Test exporting stargazers data."""
        # Mock data
        mock_response = b'{"data": "example json data"}'
        mock_get_raw.return_value = mock_response
        
        # Call the method
        result = self.client.export_stargazers(self.owner, self.repo, format="json")
        
        # Assertions
        mock_get_raw.assert_called_once_with(
            f"repos/{self.owner}/{self.repo}/stargazers/export",
            params={"format": "json"},
            accept_format="application/json"
        )
        self.assertEqual(result, mock_response)
    
    @patch('stargazers_advanced.GitHubAPIClient.get')
    def test_get_user_star_recommendations(self, mock_get):
        """Test getting repository recommendations."""
        # Mock data
        mock_response = [
            {"name": "repo1", "owner": {"login": "user1"}, "stars": 100},
            {"name": "repo2", "owner": {"login": "user2"}, "stars": 50}
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_user_star_recommendations(limit=5)
        
        # Assertions
        mock_get.assert_called_once_with(
            "user/recommendations/repositories",
            params={"limit": 5}
        )
        self.assertEqual(result, mock_response)


class TestGitHubAPIClient(unittest.TestCase):
    """Test cases for the GitHubAPIClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "https://api.github.com"
        self.api_key = "test_api_key"
        self.client = GitHubAPIClient(self.base_url, self.api_key)
    
    @patch('requests.Session.get')
    def test_get_request_success(self, mock_get):
        """Test successful GET request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get("test/endpoint", params={"param": "value"})
        
        # Assertions
        mock_get.assert_called_once_with(
            f"{self.base_url}/test/endpoint", 
            params={"param": "value"}, 
            headers=None
        )
        self.assertEqual(result, {"data": "test"})
    
    @patch('requests.Session.get')
    def test_get_request_rate_limit(self, mock_get):
        """Test GET request handling rate limiting."""
        # First response is rate limited, second is successful
        rate_limited_response = Mock()
        rate_limited_response.status_code = 429
        rate_limited_response.headers = {"Retry-After": "1"}
        
        success_response = Mock()
        success_response.status_code = 200
        success_response.content = b'{"data": "test"}'
        success_response.json.return_value = {"data": "test"}
        
        mock_get.side_effect = [rate_limited_response, success_response]
        
        # Patch time.sleep to avoid waiting during test
        with patch('time.sleep'):
            # Call the method
            result = self.client.get("test/endpoint")
            
            # Assertions
            self.assertEqual(mock_get.call_count, 2)
            self.assertEqual(result, {"data": "test"})
    
    @patch('requests.Session.get')
    def test_get_request_retry_on_error(self, mock_get):
        """Test GET request retrying on network error."""
        # First response raises exception, second is successful
        mock_get.side_effect = [
            requests.exceptions.ConnectionError("Network error"),
            Mock(status_code=200, content=b'{"data": "test"}', json=lambda: {"data": "test"})
        ]
        
        # Patch time.sleep to avoid waiting during test
        with patch('time.sleep'):
            # Call the method
            result = self.client.get("test/endpoint")
            
            # Assertions
            self.assertEqual(mock_get.call_count, 2)
            self.assertEqual(result, {"data": "test"})
    
    @patch('requests.Session.get')
    def test_get_request_max_retries_exceeded(self, mock_get):
        """Test GET request exceeding maximum retries."""
        # All responses raise exceptions
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        # Patch time.sleep to avoid waiting during test
        with patch('time.sleep'):
            # Call the method and expect exception
            with self.assertRaises(requests.exceptions.ConnectionError):
                self.client.get("test/endpoint")
            
            # Assert we tried the maximum number of times
            self.assertEqual(mock_get.call_count, 4)  # Initial + 3 retries
    
    @patch('requests.Session.post')
    def test_post_request(self, mock_post):
        """Test POST request."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.content = b'{"id": 123}'
        mock_response.json.return_value = {"id": 123}
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.client.post(
            "test/endpoint", 
            data={"name": "test"}, 
            params={"param": "value"}
        )
        
        # Assertions
        mock_post.assert_called_once_with(
            f"{self.base_url}/test/endpoint", 
            params={"param": "value"}, 
            json={"name": "test"}, 
            headers=None
        )
        self.assertEqual(result, {"id": 123})


if __name__ == '__main__':
    unittest.main()
