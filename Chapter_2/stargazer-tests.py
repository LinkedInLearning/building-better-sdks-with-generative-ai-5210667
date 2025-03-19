import unittest
from unittest.mock import patch, MagicMock
from stargazers import GitHubAPI

class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        self.token = "test_token"
        self.github = GitHubAPI(self.token)

    @patch('requests.get')
    def test_get_repository(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Hello-World"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        repo = self.github.get_repository("octocat", "Hello-World")
        self.assertEqual(repo, {"id": 1, "name": "Hello-World"})
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/octocat/Hello-World",
            headers=self.github.headers
        )

    @patch('requests.post')
    def test_create_issue(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "title": "New issue"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        issue = self.github.create_issue("octocat", "Hello-World", "New issue title", "Issue body")
        self.assertEqual(issue, {"id": 1, "title": "New issue"})
        mock_post.assert_called_once_with(
            "https://api.github.com/repos/octocat/Hello-World/issues",
            headers=self.github.headers,
            json={
                "title": "New issue title",
                "body": "Issue body",
                "assignees": None,
                "labels": None
            }
        )

    @patch('requests.get')
    def test_list_issues(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "title": "Issue 1"}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        issues = self.github.list_issues("octocat", "Hello-World")
        self.assertEqual(issues, [{"id": 1, "title": "Issue 1"}])
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/octocat/Hello-World/issues",
            headers=self.github.headers,
            params={"state": "open"}
        )

    @patch('requests.get')
    def test_list_stargazers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"login": "octocat"}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        stargazers = self.github.list_stargazers("octocat", "Hello-World")
        self.assertEqual(stargazers, [{"login": "octocat"}])
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/octocat/Hello-World/stargazers",
            headers=self.github.headers
        )

    @patch('requests.get')
    def test_list_starred_repositories(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "name": "Hello-World"}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        starred_repos = self.github.list_starred_repositories("octocat")
        self.assertEqual(starred_repos, [{"id": 1, "name": "Hello-World"}])
        mock_get.assert_called_once_with(
            "https://api.github.com/users/octocat/starred",
            headers=self.github.headers
        )

    @patch('requests.get')
    def test_check_if_starred(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_get.return_value = mock_response

        is_starred = self.github.check_if_starred("octocat", "Hello-World")
        self.assertTrue(is_starred)
        mock_get.assert_called_once_with(
            "https://api.github.com/user/starred/octocat/Hello-World",
            headers=self.github.headers
        )

    @patch('requests.put')
    def test_star_repository(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_put.return_value = mock_response

        star_status = self.github.star_repository("octocat", "Hello-World")
        self.assertTrue(star_status)
        mock_put.assert_called_once_with(
            "https://api.github.com/user/starred/octocat/Hello-World",
            headers=self.github.headers
        )

    @patch('requests.delete')
    def test_unstar_repository(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        unstar_status = self.github.unstar_repository("octocat", "Hello-World")
        self.assertTrue(unstar_status)
        mock_delete.assert_called_once_with(
            "https://api.github.com/user/starred/octocat/Hello-World",
            headers=self.github.headers
        )

if __name__ == "__main__":
    unittest.main()