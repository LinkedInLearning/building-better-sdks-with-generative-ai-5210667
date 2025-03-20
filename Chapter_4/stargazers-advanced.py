import requests
import json
import time
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import logging


class GitHubAPIClient:
    """
    Base class for GitHub API clients that handles authentication, error handling, and retry logic.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize the base GitHub API client.
        
        Args:
            base_url: The base URL for the GitHub API
            api_key: Optional API key or access token for authentication
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Initial delay between retries in seconds (will increase exponentially)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create and configure the session
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        # Add authentication if provided
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def _make_request(self, method: str, endpoint: str, 
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Make an HTTP request with retry logic and error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint to call (relative to base_url)
            params: Optional query parameters
            data: Optional request body data (will be converted to JSON)
            headers: Optional additional headers
            
        Returns:
            Response object from successful request
            
        Raises:
            requests.exceptions.HTTPError: If request fails even after retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        retries = 0
        delay = self.retry_delay
        
        while retries <= self.max_retries:
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, headers=request_headers)
                elif method.upper() == 'POST':
                    response = self.session.post(url, params=params, json=data, headers=request_headers)
                elif method.upper() == 'PUT':
                    response = self.session.put(url, params=params, json=data, headers=request_headers)
                elif method.upper() == 'PATCH':
                    response = self.session.patch(url, params=params, json=data, headers=request_headers)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, params=params, headers=request_headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Check if request was successful
                if response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', delay))
                    self.logger.warning(f"Rate limited. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                    retries += 1
                    delay *= 2  # Exponential backoff
                    continue
                    
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                # Determine if we should retry
                if retries >= self.max_retries:
                    self.logger.error(f"Request failed after {retries} retries: {str(e)}")
                    raise
                
                retries += 1
                self.logger.warning(f"Request failed, retrying ({retries}/{self.max_retries}): {str(e)}")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
        
        # This should not be reached, but just in case
        raise requests.exceptions.RequestException("Max retries exceeded with no successful response")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
           headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint to call
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Parsed JSON response as Python object
        """
        response = self._make_request('GET', endpoint, params=params, headers=headers)
        return response.json() if response.content else None
    
    def post(self, endpoint: str, data: Dict[str, Any], 
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint to call
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Parsed JSON response as Python object
        """
        response = self._make_request('POST', endpoint, params=params, data=data, headers=headers)
        return response.json() if response.content else None
    
    def put(self, endpoint: str, data: Dict[str, Any], 
           params: Optional[Dict[str, Any]] = None,
           headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint to call
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Parsed JSON response as Python object
        """
        response = self._make_request('PUT', endpoint, params=params, data=data, headers=headers)
        return response.json() if response.content else None
    
    def patch(self, endpoint: str, data: Dict[str, Any], 
             params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a PATCH request to the API.
        
        Args:
            endpoint: API endpoint to call
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Parsed JSON response as Python object
        """
        response = self._make_request('PATCH', endpoint, params=params, data=data, headers=headers)
        return response.json() if response.content else None
    
    def delete(self, endpoint: str, 
              params: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None) -> Any:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint to call
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Parsed JSON response as Python object (if any)
        """
        response = self._make_request('DELETE', endpoint, params=params, headers=headers)
        return response.json() if response.content else None
    
    def get_raw(self, endpoint: str, 
               params: Optional[Dict[str, Any]] = None,
               accept_format: Optional[str] = None) -> bytes:
        """
        Make a GET request and return the raw response content.
        
        Args:
            endpoint: API endpoint to call
            params: Optional query parameters
            accept_format: Optional content type to request
            
        Returns:
            Raw response content as bytes
        """
        headers = {}
        if accept_format:
            headers["Accept"] = accept_format
            
        response = self._make_request('GET', endpoint, params=params, headers=headers)
        return response.content


class GitHubStarsClient:
    """
    Client for GitHub API operations related to stars and stargazers.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None,
                max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize the GitHub Stars client.
        
        Args:
            base_url: The base URL for the GitHub API
            api_key: Optional API key or access token for authentication
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Initial delay between retries in seconds
        """
        self.api = GitHubAPIClient(base_url, api_key, max_retries, retry_delay)
    
    # Star-related methods
    def list_repository_stars(self, owner: str, repo: str, 
                             per_page: Optional[int] = None, 
                             page: Optional[int] = None,
                             sort: Optional[str] = None) -> Dict[str, Any]:
        """
        List stargazers of a repository with pagination.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            per_page: Number of results per page
            page: Page number to retrieve
            sort: Sort order (created, updated)
            
        Returns:
            Dictionary containing stargazer data and pagination info
        """
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        if sort is not None:
            params['sort'] = sort
            
        return self.api.get(f"repos/{owner}/{repo}/stargazers", params=params)
    
    def star_repository(self, owner: str, repo: str) -> None:
        """
        Star a repository.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
        """
        self.api.put(f"user/starred/{owner}/{repo}", data={})
    
    def unstar_repository(self, owner: str, repo: str) -> None:
        """
        Unstar a repository.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
        """
        self.api.delete(f"user/starred/{owner}/{repo}")
    
    def check_starred(self, owner: str, repo: str) -> bool:
        """
        Check if the authenticated user has starred a repository.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            
        Returns:
            Boolean indicating whether the repository is starred
        """
        try:
            self.api.get(f"user/starred/{owner}/{repo}")
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False
            raise
    
    def list_starred_repositories(self, username: Optional[str] = None, 
                                 per_page: Optional[int] = None,
                                 page: Optional[int] = None,
                                 sort: Optional[str] = None,
                                 direction: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List repositories starred by a user.
        
        Args:
            username: Username (if None, returns authenticated user's starred repos)
            per_page: Number of results per page
            page: Page number to retrieve
            sort: Sort by (created, updated)
            direction: Sort direction (asc, desc)
            
        Returns:
            List of dictionaries containing repository information
        """
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        if sort is not None:
            params['sort'] = sort
        if direction is not None:
            params['direction'] = direction
            
        endpoint = f"users/{username}/starred" if username else "user/starred"
        return self.api.get(endpoint, params=params)
    
    def get_star_count(self, owner: str, repo: str) -> int:
        """
        Get the total count of stars for a repository.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            
        Returns:
            Integer count of stars
        """
        repo_info = self.api.get(f"repos/{owner}/{repo}")
        return repo_info.get("stargazers_count", 0)
    
    def get_star_history(self, owner: str, repo: str, 
                        per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Get historical data of stars for a repository with timestamps.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            per_page: Number of results per page
            
        Returns:
            List of dictionaries containing stargazer information with timestamps
        """
        # GitHub API requires a specific Accept header to get timestamps
        headers = {"Accept": "application/vnd.github.v3.star+json"}
        
        # Initial request
        params = {"per_page": per_page, "page": 1}
        star_history = self.api.get(f"repos/{owner}/{repo}/stargazers", 
                                   params=params, 
                                   headers=headers)
        
        all_stars = star_history.copy()
        
        # Get link header to check for pagination
        # This is a simplified implementation that would need more work
        # to properly handle GitHub's pagination links
        while len(star_history) == per_page:
            params["page"] += 1
            try:
                star_history = self.api.get(f"repos/{owner}/{repo}/stargazers", 
                                          params=params, 
                                          headers=headers)
                all_stars.extend(star_history)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    break
                raise
        
        return all_stars
    
    def get_trending_repositories(self, language: Optional[str] = None,
                                 since: Optional[str] = None,
                                 spoken_language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get trending repositories based on stars.
        
        Args:
            language: Filter by programming language
            since: Time period (daily, weekly, monthly)
            spoken_language: Filter by natural language
            
        Returns:
            List of dictionaries containing trending repository information
        """
        params = {}
        if language:
            params["language"] = language
        if since:
            params["since"] = since
        if spoken_language:
            params["spoken_language_code"] = spoken_language
            
        return self.api.get("trending/repositories", params=params)
    
    def export_stargazers(self, owner: str, repo: str, 
                         format: str = "json") -> bytes:
        """
        Export the list of stargazers for a repository in the specified format.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            format: Export format (json, csv)
            
        Returns:
            Bytes containing the exported data
        """
        accept_format = f"application/{format}"
        endpoint = f"repos/{owner}/{repo}/stargazers/export"
        params = {"format": format}
        
        return self.api.get_raw(endpoint, params=params, accept_format=accept_format)
    
    def get_user_star_recommendations(self, limit: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Get repository recommendations based on user's starring history.
        
        Args:
            limit: Maximum number of recommendations to return
            
        Returns:
            List of dictionaries containing recommended repositories
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
            
        return self.api.get("user/recommendations/repositories", params=params)


# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = GitHubStarsClient("https://api.github.com", api_key="your_github_token")
    
    # List stargazers for a repository
    stars = client.list_repository_stars("octocat", "hello-world", per_page=10)
    print(f"Repository has {len(stars)} recent stargazers")
    
    # Star a repository
    client.star_repository("octocat", "hello-world")
    print("Repository starred successfully")
    
    # Check if a repository is starred
    is_starred = client.check_starred("octocat", "hello-world")
    print(f"Repository is starred: {is_starred}")
    
    # Get total star count for a repository
    count = client.get_star_count("octocat", "hello-world")
    print(f"Repository has {count} stars in total")
    
    # List repositories starred by a user
    starred_repos = client.list_starred_repositories("octocat", per_page=5, sort="updated")
    print(f"User has starred {len(starred_repos)} repositories")
    
    # Get trending repositories
    trending = client.get_trending_repositories(language="python", since="weekly")
    print("Trending Python repositories this week:")
    for repo in trending:
        print(f"- {repo['full_name']}: {repo['stargazers_count']} stars")