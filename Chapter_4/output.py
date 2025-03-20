import requests
import time
from typing import Dict, List, Optional, Union, Any

class GitHubAPI:
    """
    Python client for GitHub Enterprise Cloud API
    Based on API version 2022-11-28
    """
    
    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """
        Initialize the GitHub API client
        
        Args:
            token: GitHub personal access token
            base_url: API base URL (default: https://api.github.com)
        """
        self.token = token
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Any:
        """
        Make a request to the GitHub API
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (e.g., /repos/{owner}/{repo})
            data: Request body data for POST, PUT, PATCH requests
            params: URL parameters
            headers: Additional headers
            
        Returns:
            API response (parsed JSON or None for 204 responses)
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = self.headers.copy()
        
        if headers:
            request_headers.update(headers)
            
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params,
                headers=request_headers
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = max(reset_time - time.time(), 0) + 1
                print(f"Rate limit exceeded. Waiting for {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                return self._request(method, endpoint, data, params, headers)
                
            response.raise_for_status()
            
            # Return None for 204 No Content responses
            if response.status_code == 204:
                return None
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Try to get error details from response
            try:
                error_data = e.response.json()
                raise Exception(f"GitHub API Error: {e.response.status_code} - {error_data.get('message', str(e))}")
            except (ValueError, AttributeError):
                raise Exception(f"GitHub API Error: {str(e)}")
    
    def paginate(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Automatically handle pagination for list endpoints
        
        Args:
            endpoint: API endpoint
            params: URL parameters
            
        Returns:
            List of all items across all pages
        """
        all_items = []
        params = params or {}
        params['per_page'] = params.get('per_page', 100)
        page = 1
        
        while True:
            params['page'] = page
            response = self._request('GET', endpoint, params=params)
            
            if not response or not isinstance(response, list) or len(response) == 0:
                break
                
            all_items.extend(response)
            
            if len(response) < params['per_page']:
                break
                
            page += 1
            
        return all_items
        
    # Repository operations
    def list_repositories(self, org: str, type: str = 'all', sort: str = 'updated', 
                         direction: str = 'desc') -> List[Dict]:
        """
        List repositories for an organization
        
        Args:
            org: Organization name
            type: Type of repositories to include (all, public, private, forks, sources, member, internal)
            sort: Property to sort by (created, updated, pushed, full_name)
            direction: Sort direction (asc or desc)
            
        Returns:
            List of repositories
        """
        params = {
            'type': type,
            'sort': sort,
            'direction': direction
        }
        return self.paginate(f'/orgs/{org}/repos', params)
    
    def get_repository(self, owner: str, repo: str) -> Dict:
        """
        Get a repository
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            
        Returns:
            Repository details
        """
        return self._request('GET', f'/repos/{owner}/{repo}')
    
    def create_repository(self, name: str, org: Optional[str] = None, **kwargs) -> Dict:
        """
        Create a repository
        
        Args:
            name: Repository name
            org: Organization name (if creating under an organization)
            **kwargs: Optional repository parameters
                - description: Repository description
                - homepage: Repository website
                - private: Whether the repository is private
                - has_issues: Enable issues feature
                - has_projects: Enable projects feature
                - has_wiki: Enable wiki feature
                - has_downloads: Enable downloads feature
                - team_id: Team ID that will be granted access
                - auto_init: Create initial commit with empty README
                - gitignore_template: Gitignore template to use
                - license_template: License template to use
                - allow_squash_merge: Allow squash merges
                - allow_merge_commit: Allow merge commits
                - allow_rebase_merge: Allow rebase merges
                - delete_branch_on_merge: Delete head branch on merge
                
        Returns:
            Created repository details
        """
        data = {'name': name, **kwargs}
        
        if org:
            return self._request('POST', f'/orgs/{org}/repos', data=data)
        else:
            return self._request('POST', '/user/repos', data=data)
    
    def update_repository(self, owner: str, repo: str, **kwargs) -> Dict:
        """
        Update a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            **kwargs: Repository properties to update
            
        Returns:
            Updated repository details
        """
        return self._request('PATCH', f'/repos/{owner}/{repo}', data=kwargs)
    
    def delete_repository(self, owner: str, repo: str) -> None:
        """
        Delete a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
        """
        return self._request('DELETE', f'/repos/{owner}/{repo}')
    
    # Branch operations
    def list_branches(self, owner: str, repo: str, protected: Optional[bool] = None) -> List[Dict]:
        """
        List branches for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            protected: Filter by branch protection status
            
        Returns:
            List of branches
        """
        params = {}
        if protected is not None:
            params['protected'] = str(protected).lower()
            
        return self.paginate(f'/repos/{owner}/{repo}/branches', params)
    
    def get_branch(self, owner: str, repo: str, branch: str) -> Dict:
        """
        Get a branch
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name
            
        Returns:
            Branch details
        """
        return self._request('GET', f'/repos/{owner}/{repo}/branches/{branch}')
    
    # Issue operations
    def list_issues(self, owner: str, repo: str, state: str = 'open', 
                   sort: str = 'created', direction: str = 'desc') -> List[Dict]:
        """
        List issues for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            sort: Property to sort by (created, updated, comments)
            direction: Sort direction (asc or desc)
            
        Returns:
            List of issues
        """
        params = {
            'state': state,
            'sort': sort,
            'direction': direction
        }
        return self.paginate(f'/repos/{owner}/{repo}/issues', params)
    
    def get_issue(self, owner: str, repo: str, issue_number: int) -> Dict:
        """
        Get an issue
        
        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            
        Returns:
            Issue details
        """
        return self._request('GET', f'/repos/{owner}/{repo}/issues/{issue_number}')
    
    def create_issue(self, owner: str, repo: str, title: str, body: Optional[str] = None, **kwargs) -> Dict:
        """
        Create an issue
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body
            **kwargs: Optional issue parameters
                - assignees: List of user logins to assign
                - milestone: Milestone ID
                - labels: List of label names
                
        Returns:
            Created issue details
        """
        data = {'title': title, **kwargs}
        if body:
            data['body'] = body
            
        return self._request('POST', f'/repos/{owner}/{repo}/issues', data=data)
    
    def update_issue(self, owner: str, repo: str, issue_number: int, **kwargs) -> Dict:
        """
        Update an issue
        
        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            **kwargs: Issue properties to update
            
        Returns:
            Updated issue details
        """
        return self._request('PATCH', f'/repos/{owner}/{repo}/issues/{issue_number}', data=kwargs)
    
    # Pull request operations
    def list_pull_requests(self, owner: str, repo: str, state: str = 'open',
                          sort: str = 'created', direction: str = 'desc') -> List[Dict]:
        """
        List pull requests for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Pull request state (open, closed, all)
            sort: Property to sort by (created, updated, popularity, long-running)
            direction: Sort direction (asc or desc)
            
        Returns:
            List of pull requests
        """
        params = {
            'state': state,
            'sort': sort,
            'direction': direction
        }
        return self.paginate(f'/repos/{owner}/{repo}/pulls', params)
    
    def get_pull_request(self, owner: str, repo: str, pull_number: int) -> Dict:
        """
        Get a pull request
        
        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            
        Returns:
            Pull request details
        """
        return self._request('GET', f'/repos/{owner}/{repo}/pulls/{pull_number}')
    
    def create_pull_request(self, owner: str, repo: str, title: str, head: str, base: str, 
                           body: Optional[str] = None, **kwargs) -> Dict:
        """
        Create a pull request
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Pull request title
            head: Head branch name
            base: Base branch name
            body: Pull request description
            **kwargs: Optional pull request parameters
                - draft: Submit as draft pull request
                - maintainer_can_modify: Allow maintainers to modify head branch
                
        Returns:
            Created pull request details
        """
        data = {
            'title': title,
            'head': head,
            'base': base,
            **kwargs
        }
        if body:
            data['body'] = body
            
        return self._request('POST', f'/repos/{owner}/{repo}/pulls', data=data)
    
    def update_pull_request(self, owner: str, repo: str, pull_number: int, **kwargs) -> Dict:
        """
        Update a pull request
        
        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            **kwargs: Pull request properties to update
            
        Returns:
            Updated pull request details
        """
        return self._request('PATCH', f'/repos/{owner}/{repo}/pulls/{pull_number}', data=kwargs)
    
    def merge_pull_request(self, owner: str, repo: str, pull_number: int, 
                          commit_message: Optional[str] = None, 
                          merge_method: str = 'merge') -> Dict:
        """
        Merge a pull request
        
        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            commit_message: Custom commit message
            merge_method: Merge method (merge, squash, rebase)
            
        Returns:
            Merge result
        """
        data = {'merge_method': merge_method}
        if commit_message:
            data['commit_message'] = commit_message
            
        return self._request('PUT', f'/repos/{owner}/{repo}/pulls/{pull_number}/merge', data=data)
    
    # Organization operations
    def list_organizations(self) -> List[Dict]:
        """
        List organizations for the authenticated user
        
        Returns:
            List of organizations
        """
        return self.paginate('/user/orgs')
    
    def get_organization(self, org: str) -> Dict:
        """
        Get an organization
        
        Args:
            org: Organization name
            
        Returns:
            Organization details
        """
        return self._request('GET', f'/orgs/{org}')
    
    def list_organization_members(self, org: str, role: str = 'all') -> List[Dict]:
        """
        List members of an organization
        
        Args:
            org: Organization name
            role: Filter by role (all, admin, member)
            
        Returns:
            List of organization members
        """
        params = {'role': role}
        return self.paginate(f'/orgs/{org}/members', params)
    
    # Team operations
    def list_teams(self, org: str) -> List[Dict]:
        """
        List teams in an organization
        
        Args:
            org: Organization name
            
        Returns:
            List of teams
        """
        return self.paginate(f'/orgs/{org}/teams')
    
    def get_team(self, org: str, team_slug: str) -> Dict:
        """
        Get a team
        
        Args:
            org: Organization name
            team_slug: Team slug
            
        Returns:
            Team details
        """
        return self._request('GET', f'/orgs/{org}/teams/{team_slug}')
    
    def list_team_members(self, org: str, team_slug: str, role: str = 'all') -> List[Dict]:
        """
        List members of a team
        
        Args:
            org: Organization name
            team_slug: Team slug
            role: Filter by role (all, maintainer, member)
            
        Returns:
            List of team members
        """
        params = {'role': role}
        return self.paginate(f'/orgs/{org}/teams/{team_slug}/members', params)
    
    # User operations
    def get_authenticated_user(self) -> Dict:
        """
        Get the authenticated user
        
        Returns:
            User details
        """
        return self._request('GET', '/user')
    
    def get_user(self, username: str) -> Dict:
        """
        Get a user
        
        Args:
            username: Username
            
        Returns:
            User details
        """
        return self._request('GET', f'/users/{username}')
    
    # Workflow operations
    def list_workflows(self, owner: str, repo: str) -> Dict:
        """
        List workflows in a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of workflows
        """
        return self._request('GET', f'/repos/{owner}/{repo}/actions/workflows')
    
    def get_workflow(self, owner: str, repo: str, workflow_id: Union[int, str]) -> Dict:
        """
        Get a workflow
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID or filename
            
        Returns:
            Workflow details
        """
        return self._request('GET', f'/repos/{owner}/{repo}/actions/workflows/{workflow_id}')
    
    def list_workflow_runs(self, owner: str, repo: str, workflow_id: Union[int, str],
                          status: Optional[str] = None) -> Dict:
        """
        List workflow runs
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID or filename
            status: Filter by status (queued, in_progress, completed, etc.)
            
        Returns:
            List of workflow runs
        """
        params = {}
        if status:
            params['status'] = status
            
        return self._request('GET', f'/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs', params=params)
    
    # Content operations
    def get_content(self, owner: str, repo: str, path: str, ref: Optional[str] = None) -> Dict:
        """
        Get repository content
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Path to the content
            ref: The name of the commit/branch/tag
            
        Returns:
            Content details
        """
        params = {}
        if ref:
            params['ref'] = ref
            
        return self._request('GET', f'/repos/{owner}/{repo}/contents/{path}', params=params)
    
    def create_or_update_file(self, owner: str, repo: str, path: str, message: str, 
                             content: str, branch: Optional[str] = None,
                             sha: Optional[str] = None) -> Dict:
        """
        Create or update a file
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Path to the file
            message: Commit message
            content: Base64 encoded content
            branch: Branch name (default: repository's default branch)
            sha: File SHA (required for updating existing files)
            
        Returns:
            Created/updated file details
        """
        data = {
            'message': message,
            'content': content
        }
        
        if branch:
            data['branch'] = branch
            
        if sha:
            data['sha'] = sha
            
        return self._request('PUT', f'/repos/{owner}/{repo}/contents/{path}', data=data)


# Example usage
def example_usage():
    """Example usage of the GitHub API client"""
    
    # Create a GitHub API client
    github = GitHubAPI("your_personal_access_token")
    
    try:
        # Get authenticated user info
        user = github.get_authenticated_user()
        print(f"Authenticated as: {user['login']}")
        
        # Get a specific repository
        repo = github.get_repository("octocat", "hello-world")
        print(f"Repository: {repo['full_name']}")
        print(f"Description: {repo['description']}")
        print(f"Stars: {repo['stargazers_count']}")
        
        # List organization repositories
        repos = github.list_repositories("github")
        print(f"Found {len(repos)} repositories in the 'github' organization")
        
        # Create a new repository
        new_repo = github.create_repository(
            name="test-repo",
            org="your-organization",
            description="A test repository",
            private=True,
            has_issues=True,
            has_wiki=True
        )
        print(f"Created new repository: {new_repo['html_url']}")
        
        # Create an issue
        issue = github.create_issue(
            owner="your-organization",
            repo="test-repo",
            title="Test issue",
            body="This is a test issue created via the API",
            labels=["bug", "documentation"]
        )
        print(f"Created issue #{issue['number']}: {issue['title']}")
        
        # Create a pull request
        pr = github.create_pull_request(
            owner="your-organization",
            repo="test-repo",
            title="Add new feature",
            head="feature-branch",
            base="main",
            body="This pull request adds an awesome new feature",
            draft=False
        )
        print(f"Created PR #{pr['number']}: {pr['title']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    example_usage()