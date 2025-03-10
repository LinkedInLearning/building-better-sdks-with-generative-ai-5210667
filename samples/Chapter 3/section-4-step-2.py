import requests

class GitHubAPI:
    def __init__(self, token, base_url="https://api.github.com"):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def list_issues(self, owner, repo, state="open"):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_issue(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
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

    def update_issue(self, owner, repo, issue_number, title=None, body=None, state=None, assignees=None, labels=None):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
        data = {
            "title": title,
            "body": body,
            "state": state,
            "assignees": assignees,
            "labels": labels
        }
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def lock_issue(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/lock"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

    def unlock_issue(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/lock"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

    def add_assignees(self, owner, repo, issue_number, assignees):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/assignees"
        data = {"assignees": assignees}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def remove_assignees(self, owner, repo, issue_number, assignees):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/assignees"
        data = {"assignees": assignees}
        response = requests.delete(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def list_issue_comments(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_issue_comment(self, owner, repo, issue_number, body):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        data = {"body": body}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_issue_comment(self, owner, repo, comment_id, body):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/comments/{comment_id}"
        data = {"body": body}
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_issue_comment(self, owner, repo, comment_id):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/comments/{comment_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

# Example usage:
if __name__ == "__main__":
    token = "your_github_token"
    github = GitHubAPI(token)

    # List issues
    issues = github.list_issues("octocat", "Hello-World")
    print(issues)

    # Get a single issue
    issue = github.get_issue("octocat", "Hello-World", 1)
    print(issue)

    # Create a new issue
    new_issue = github.create_issue("octocat", "Hello-World", "New issue title", "Issue body")
    print(new_issue)

    # Update an issue
    updated_issue = github.update_issue("octocat", "Hello-World", 1, title="Updated title")
    print(updated_issue)

    # Lock an issue
    lock_status = github.lock_issue("octocat", "Hello-World", 1)
    print(lock_status)

    # Unlock an issue
    unlock_status = github.unlock_issue("octocat", "Hello-World", 1)
    print(unlock_status)

    # Add assignees to an issue
    assignees_added = github.add_assignees("octocat", "Hello-World", 1, ["octocat"])
    print(assignees_added)

    # Remove assignees from an issue
    assignees_removed = github.remove_assignees("octocat", "Hello-World", 1, ["octocat"])
    print(assignees_removed)

    # List issue comments
    comments = github.list_issue_comments("octocat", "Hello-World", 1)
    print(comments)

    # Create an issue comment
    new_comment = github.create_issue_comment("octocat", "Hello-World", 1, "This is a comment")
    print(new_comment)

    # Update an issue comment
    updated_comment = github.update_issue_comment("octocat", "Hello-World", 1, "Updated comment")
    print(updated_comment)

    # Delete an issue comment
    delete_status = github.delete_issue_comment("octocat", "Hello-World", 1)
    print(delete_status)