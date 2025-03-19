import requests

class GitHubAPI:
    def __init__(self, token, base_url="https://api.github.com"):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_repository(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_issue(self, owner, repo, title, body=None, assignees=None, labels=None):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "labels": labels
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def list_issues(self, owner, repo, state="open"):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def list_stargazers(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/stargazers"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_starred_repositories(self, username):
        url = f"{self.base_url}/users/{username}/starred"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def check_if_starred(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 204

    def star_repository(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

    def unstar_repository(self, owner, repo):
        url = f"{self.base_url}/user/starred/{owner}/{repo}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

# Example usage:
if __name__ == "__main__":
    token = "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"
    github = GitHubAPI(token)

    # List stargazers for a repository
    stargazers = github.list_stargazers("octocat", "Hello-World")
    print(len(stargazers))

    # List repositories being starred by a user
    starred_repos = github.list_starred_repositories("octocat")
    print(len(starred_repos))

    # Check if a repository is starred by the authenticated user
    is_starred = github.check_if_starred("octocat", "Hello-World")
    print(is_starred)

    # Star a repository for the authenticated user
    star_status = github.star_repository("octocat", "Hello-World")
    print(star_status)

    # Unstar a repository for the authenticated user
    unstar_status = github.unstar_repository("octocat", "Hello-World")
    print(unstar_status)