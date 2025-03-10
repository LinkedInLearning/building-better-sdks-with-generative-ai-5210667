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

# Example usage:
if __name__ == "__main__":
    token = "your_github_token"
    github = GitHubAPI(token)

    # Get repository details
    repo = github.get_repository("octocat", "Hello-World")
    print(repo)

    # Create a new issue
    issue = github.create_issue("octocat", "Hello-World", "New issue title", "Issue body")
    print(issue)

    # List open issues
    issues = github.list_issues("octocat", "Hello-World")
    print(issues)