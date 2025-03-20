import requests
from typing import Dict, List, Optional, Union, Any

def star_repository(token: str, owner: str, repo: str) -> None:
    """
    Star a repository
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        
    Returns:
        None on success
        
    Endpoint: PUT /user/starred/{owner}/{repo}
    """
    url = f"https://api.github.com/user/starred/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.put(url, headers=headers)
    response.raise_for_status()
    return None  # Returns 204 No Content on success

def unstar_repository(token: str, owner: str, repo: str) -> None:
    """
    Unstar a repository
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        
    Returns:
        None on success
        
    Endpoint: DELETE /user/starred/{owner}/{repo}
    """
    url = f"https://api.github.com/user/starred/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return None  # Returns 204 No Content on success

def check_if_starred(token: str, owner: str, repo: str) -> bool:
    """
    Check if the authenticated user has starred a repository
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        
    Returns:
        True if repository is starred, False if not
        
    Endpoint: GET /user/starred/{owner}/{repo}
    """
    url = f"https://api.github.com/user/starred/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    
    # 204 No Content if starred, 404 Not Found if not starred
    if response.status_code == 204:
        return True
    elif response.status_code == 404:
        return False
    else:
        response.raise_for_status()

def list_starred_repositories(token: str, username: Optional[str] = None, 
                             sort: str = "created", direction: str = "desc", 
                             per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List repositories starred by a user
    
    Args:
        token: GitHub personal access token
        username: GitHub username (if None, lists repositories starred by authenticated user)
        sort: Sort by "created" (when starred) or "updated" (default: "created")
        direction: Sort direction, "asc" or "desc" (default: "desc")
        per_page: Results per page (default: 30, max: 100)
        page: Page number (default: 1)
        
    Returns:
        List of starred repositories
        
    Endpoint: 
        - GET /user/starred (authenticated user)
        - GET /users/{username}/starred (specific user)
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page
    }
    
    if username:
        url = f"https://api.github.com/users/{username}/starred"
    else:
        url = "https://api.github.com/user/starred"
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def list_stargazers(token: str, owner: str, repo: str, per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List users who have starred a repository
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        per_page: Results per page (default: 30, max: 100)
        page: Page number (default: 1)
        
    Returns:
        List of users who starred the repository
        
    Endpoint: GET /repos/{owner}/{repo}/stargazers
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "per_page": per_page,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_starred_count(token: str, owner: str, repo: str) -> int:
    """
    Get the number of stars for a repository
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        
    Returns:
        Number of stars (stargazers count)
        
    Endpoint: GET /repos/{owner}/{repo}
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["stargazers_count"]

def list_repositories_starred_by_user_with_timestamps(token: str, username: Optional[str] = None, 
                                                     per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List repositories starred by a user with star creation timestamps
    
    Args:
        token: GitHub personal access token
        username: GitHub username (if None, lists repositories starred by authenticated user)
        per_page: Results per page (default: 30, max: 100)
        page: Page number (default: 1)
        
    Returns:
        List of starred repositories with star timestamps
        
    Endpoint: 
        - GET /user/starred (authenticated user)
        - GET /users/{username}/starred (specific user)
        
    Note: This uses the star application/vnd.github.star+json media type to include timestamps
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.star+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "per_page": per_page,
        "page": page
    }
    
    if username:
        url = f"https://api.github.com/users/{username}/starred"
    else:
        url = "https://api.github.com/user/starred"
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def list_stargazers_with_timestamps(token: str, owner: str, repo: str, 
                                   per_page: int = 30, page: int = 1) -> List[Dict]:
    """
    List users who have starred a repository with star creation timestamps
    
    Args:
        token: GitHub personal access token
        owner: Repository owner (user or organization)
        repo: Repository name
        per_page: Results per page (default: 30, max: 100)
        page: Page number (default: 1)
        
    Returns:
        List of users who starred the repository with timestamps
        
    Endpoint: GET /repos/{owner}/{repo}/stargazers
    
    Note: This uses the star application/vnd.github.star+json media type to include timestamps
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.star+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "per_page": per_page,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Example usage
def example_stars_usage():
    """
    Example usage of the GitHub Stars API functions
    """
    # Replace with your GitHub personal access token
    token = "your_github_token"
    
    # Star a repository
    star_repository(token, "octocat", "hello-world")
    print("Repository starred successfully")
    
    # Check if repository is starred
    is_starred = check_if_starred(token, "octocat", "hello-world")
    print(f"Repository is starred: {is_starred}")
    
    # Get star count
    star_count = get_starred_count(token, "octocat", "hello-world")
    print(f"Repository has {star_count} stars")
    
    # List repositories starred by the authenticated user (first page only)
    starred_repos = list_starred_repositories(token)
    print(f"You have starred {len(starred_repos)} repositories (first page)")
    
    # List users who starred a repository (first page only)
    stargazers = list_stargazers(token, "octocat", "hello-world")
    print(f"Found {len(stargazers)} stargazers (first page)")
    
    # Get starred repositories with timestamps
    starred_with_times = list_repositories_starred_by_user_with_timestamps(token)
    for repo in starred_with_times[:3]:  # Show first 3
        print(f"Starred {repo['repo']['full_name']} at {repo['starred_at']}")
    
    # Unstar a repository
    unstar_repository(token, "octocat", "hello-world")
    print("Repository unstarred successfully")

if __name__ == "__main__":
    example_stars_usage()