import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class GitHubAPI:
    def __init__(self, token=None, base_url="https://api.github.com"):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _request(self, method, url, **kwargs):
        response = self.session.request(method, url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Response content: {response.content}")
            raise
        return response.json()

    def get_repository(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}"
        return self._request("GET", url)

    def create_issue(self, owner, repo, title, body=None, assignees=None, labels=None):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "labels": labels
        }
        return self._request("POST", url, json=data)

    def list_issues(self, owner, repo, state="open"):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        return self._request("GET", url, params=params)

class GitHubStarsAPI(GitHubAPI):
    def list_stargazers(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/stargazers"
        return self._request("GET", url)

    def list_starred_repositories(self, username):
        url = f"{self.base_url}/users/{username}/starred"
        return self._request("GET", url)

    def check_if_starred(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = self.session.get(url, headers=self.headers)
        return response.status_code == 204

    def star_repository(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = self.session.put(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

    def unstar_repository(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = self.session.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

# Example usage:
if __name__ == "__main__":
    token = "your_github_token"
    github_stars = GitHubStarsAPI(token)

    # List stargazers for a repository
    stargazers = github_stars.list_stargazers("octocat", "Hello-World")
    print(stargazers)

    # List repositories being starred by a user
    starred_repos = github_stars.list_starred_repositories("octocat")
    print(starred_repos)

    # Check if a repository is starred by the authenticated user
    is_starred = github_stars.check_if_starred("octocat", "Hello-World")
    print(is_starred)

    # Star a repository for the authenticated user
    star_status = github_stars.star_repository("octocat", "Hello-World")
    print(star_status)

    # Unstar a repository for the authenticated user
    unstar_status = github_stars.unstar_repository("octocat", "Hello-World")
    print(unstar_status)