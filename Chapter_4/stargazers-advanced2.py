import time
import requests
import logging
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"GitHub API Error ({status_code}): {message}")


class GitHubAPIBase:
    """
    Base class for GitHub API interactions.
    Handles authentication, error handling, and retry logic.
    """
    
    def __init__(
        self, 
        base_url: str = "https://api.github.com", 
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        timeout: int = 30
    ):
        """
        Initialize a new GitHub API client.
        
        Args:
            base_url: The base URL for the GitHub API
            api_key: Optional API key or personal access token for authentication
            max_retries: Maximum number of retries for failed requests
            retry_delay: Base delay between retries in seconds
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        
        self.session = requests.Session()
        
        # Set up authentication if provided
        if api_key:
            self.session.headers.update({"Authorization": f"token {api_key}"})
        
        # Set common headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHubAPI-Python-Client"
        })
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a request to the GitHub API with retry logic and error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            params: Optional query parameters
            data: Optional request body data
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data (JSON-decoded dict/list or raw bytes)
            
        Raises:
            GitHubAPIError: If the request fails after all retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        retries = 0
        last_error = None
        
        while retries <= self.max_retries:
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers,
                    timeout=self.timeout
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    if reset_time > 0:
                        wait_time = max(reset_time - time.time(), 0) + 1
                        self.logger.warning(f"Rate limited. Waiting {wait_time:.2f} seconds.")
                        time.sleep(wait_time)
                        continue
                
                # Raise exception for client and server errors
                response.raise_for_status()
                
                # Return appropriate response format
                if raw_response:
                    return response.content
                
                if not response.content:
                    return None
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                last_error = e
                retries += 1
                
                # Break immediately on 4xx client errors (except 429)
                if hasattr(e, "response") and e.response is not None:
                    if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                        error_message = str(e)
                        try:
                            error_data = e.response.json()
                            if "message" in error_data:
                                error_message = error_data["message"]
                        except (ValueError, KeyError):
                            pass
                        
                        raise GitHubAPIError(
                            status_code=e.response.status_code,
                            message=error_message
                        )
                
                # Only retry on potential server errors or timeout issues
                if retries <= self.max_retries:
                    delay = self.retry_delay * (2 ** (retries - 1))  # Exponential backoff
                    self.logger.warning(
                        f"Request failed: {str(e)}. Retrying in {delay:.2f} seconds. "
                        f"(Attempt {retries}/{self.max_retries})"
                    )
                    time.sleep(delay)
                    continue
        
        # If we got here, all retries failed
        if isinstance(last_error, requests.exceptions.HTTPError) and last_error.response is not None:
            status_code = last_error.response.status_code
            error_message = str(last_error)
            try:
                error_data = last_error.response.json()
                if "message" in error_data:
                    error_message = error_data["message"]
            except (ValueError, KeyError):
                pass
            
            raise GitHubAPIError(status_code=status_code, message=error_message)
        
        # Generic error for non-HTTP errors (network issues, etc.)
        raise GitHubAPIError(
            status_code=0,
            message=f"Request failed after {self.max_retries} retries: {str(last_error)}"
        )
    
    def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a GET request to the GitHub API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data
        """
        return self._request("GET", endpoint, params=params, headers=headers, raw_response=raw_response)
    
    def post(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a POST request to the GitHub API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data
        """
        return self._request("POST", endpoint, params=params, data=data, headers=headers, raw_response=raw_response)
    
    def put(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a PUT request to the GitHub API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data
        """
        return self._request("PUT", endpoint, params=params, data=data, headers=headers, raw_response=raw_response)
    
    def patch(
        self, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a PATCH request to the GitHub API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            params: Optional query parameters
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data
        """
        return self._request("PATCH", endpoint, params=params, data=data, headers=headers, raw_response=raw_response)
    
    def delete(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw_response: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bytes, None]:
        """
        Make a DELETE request to the GitHub API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            headers: Optional additional headers
            raw_response: Return raw response content instead of JSON
            
        Returns:
            Response data
        """
        return self._request("DELETE", endpoint, params=params, headers=headers, raw_response=raw_response)


class GitHubStargazersAPI:
    """
    Client for interacting with GitHub Stars and Stargazers API endpoints.
    """
    
    def __init__(self, api_client: GitHubAPIBase):
        """
        Initialize the GitHub Stars API client.
        
        Args:
            api_client: GitHubAPIBase instance for making API requests
        """
        self.api = api_client
    
    def list_stargazers(
        self, 
        owner: str,
        repo: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List users who have starred the specified repository.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            per_page: Number of results per page (max 100)
            page: Page number for pagination
            sort: Sort order ("created" for starred_at date)
            
        Returns:
            Dictionary containing stargazer data and pagination info
        """
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # Use the application/vnd.github.v3.star+json accept header for timestamp info
        headers = {"Accept": "application/vnd.github.v3.star+json"} if sort == "created" else None
        
        endpoint = f"repos/{owner}/{repo}/stargazers"
        return self.api.get(endpoint, params=params, headers=headers)
    
    def star_repository(self, owner: str, repo: str) -> None:
        """
        Star a repository.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
        """
        endpoint = f"user/starred/{owner}/{repo}"
        self.api.put(endpoint)
    
    def unstar_repository(self, owner: str, repo: str) -> None:
        """
        Unstar a repository.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
        """
        endpoint = f"user/starred/{owner}/{repo}"
        self.api.delete(endpoint)
    
    def list_starred_repositories(
        self,
        username: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List repositories starred by a user.
        
        Args:
            username: GitHub username (None for authenticated user)
            sort: Sort by "created" (when starred) or "updated" (default)
            direction: Sort direction "asc" or "desc" (default)
            per_page: Number of results per page (max 100)
            page: Page number for pagination
            
        Returns:
            Dictionary containing repository data and pagination info
        """
        params = {}
        if sort is not None:
            params['sort'] = sort
        if direction is not None:
            params['direction'] = direction
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # Use the application/vnd.github.v3.star+json accept header for timestamp info
        headers = {"Accept": "application/vnd.github.v3.star+json"} if sort == "created" else None
        
        # Use the authenticated user's endpoint if username is not provided
        endpoint = f"users/{username}/starred" if username else "user/starred"
        return self.api.get(endpoint, params=params, headers=headers)
    
    def check_if_starred(self, owner: str, repo: str) -> bool:
        """
        Check if the authenticated user has starred the specified repository.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            
        Returns:
            Boolean indicating whether the repository is starred
        """
        endpoint = f"user/starred/{owner}/{repo}"
        try:
            self.api.get(endpoint)
            return True
        except GitHubAPIError as e:
            if e.status_code == 404:
                return False
            raise
    
    def get_repository_stargazer_count(self, owner: str, repo: str) -> int:
        """
        Get the number of stargazers for a repository.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            
        Returns:
            Integer count of stargazers
        """
        endpoint = f"repos/{owner}/{repo}"
        repo_data = self.api.get(endpoint)
        return repo_data.get("stargazers_count", 0)
    
    def get_star_history(
        self,
        owner: str,
        repo: str,
        max_pages: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get historical data of when users starred a repository.
        
        Note: This is an approximation built on top of the GitHub API, as there's
        no direct endpoint for star history. This method paginates through all
        stargazers with the 'created' sort to get timestamps.
        
        Args:
            owner: Repository owner (user or organization)
            repo: Repository name
            max_pages: Maximum number of pages to fetch (100 stargazers per page)
            
        Returns:
            List of dictionaries with user and starred_at information
        """
        all_stargazers = []
        page = 1
        
        while True:
            # Use the application/vnd.github.v3.star+json accept header for timestamp info
            headers = {"Accept": "application/vnd.github.v3.star+json"}
            endpoint = f"repos/{owner}/{repo}/stargazers"
            
            try:
                stargazers_page = self.api.get(
                    endpoint, 
                    params={"per_page": 100, "page": page},
                    headers=headers
                )
                
                # Break if no more results or reached max pages
                if not stargazers_page or page > max_pages:
                    break
                
                all_stargazers.extend(stargazers_page)
                page += 1
                
                # Check if we're on the last page based on Link header
                if isinstance(stargazers_page, list) and len(stargazers_page) < 100:
                    break
                    
            except GitHubAPIError as e:
                # Break on any error
                self.api.logger.error(f"Error fetching star history: {str(e)}")
                break
        
        # Process the results to extract user and time information
        history = []
        for item in all_stargazers:
            if isinstance(item, dict):
                user = item.get("user", {})
                starred_at = item.get("starred_at")
                
                if user and starred_at:
                    history.append({
                        "user_id": user.get("id"),
                        "username": user.get("login"),
                        "starred_at": starred_at
                    })
        
        return history
    
    def get_trending_repositories(
        self,
        language: Optional[str] = None,
        since: Optional[str] = "daily",
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Get trending repositories based on stars.
        
        Note: GitHub doesn't have an official trending API, so this is a simplified
        implementation using search. For production use, consider using the GitHub
        trending page scraper or a third-party API.
        
        Args:
            language: Programming language filter
            since: Time period ("daily", "weekly", "monthly")
            limit: Maximum number of repositories to return
            
        Returns:
            List of dictionaries containing repository information
        """
        # Convert the time period to GitHub search date format
        date_range = {
            "daily": "created:>=" + (datetime.now().date() - 
                                    datetime.timedelta(days=1)).isoformat(),
            "weekly": "created:>=" + (datetime.now().date() - 
                                     datetime.timedelta(weeks=1)).isoformat(),
            "monthly": "created:>=" + (datetime.now().date() - 
                                      datetime.timedelta(days=30)).isoformat()
        }.get(since, "created:>=" + (datetime.now().date() - 
                                   datetime.timedelta(days=1)).isoformat())
        
        # Construct the search query
        query = f"stars:>1 {date_range}"
        if language:
            query += f" language:{language}"
        
        # Execute the search
        search_results = self.api.get(
            "search/repositories",
            params={
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": min(limit, 100)  # API max is 100 per page
            }
        )
        
        trending = []
        if search_results and "items" in search_results:
            trending = search_results["items"][:limit]
        
        return trending


# Example usage:
if __name__ == "__main__":
    # Create the base API client
    github_api = GitHubAPIBase(api_key="your_github_token")
    
    # Create the Stars API client
    stars_api = GitHubStargazersAPI(github_api)
    
    # Use the Stars API
    try:
        # Get stargazers for a repository
        stargazers = stars_api.list_stargazers("octocat", "hello-world", per_page=10)
        print(f"First 10 stargazers: {stargazers}")
        
        # Get star count
        star_count = stars_api.get_repository_stargazer_count("octocat", "hello-world")
        print(f"Repository has {star_count} stars")
        
        # Check if authenticated user has starred a repository
        is_starred = stars_api.check_if_starred("octocat", "hello-world")
        print(f"You have{'' if is_starred else ' not'} starred this repository")
        
        # Get star history (limited to first 100 pages)
        history = stars_api.get_star_history("octocat", "hello-world", max_pages=3)
        print(f"Retrieved {len(history)} star history records")
        
        # Get trending Python repositories
        trending = stars_api.get_trending_repositories(language="python", since="weekly", limit=5)
        print("Top 5 trending Python repositories this week:")
        for repo in trending:
            print(f"- {repo['full_name']}: {repo['stargazers_count']} stars")
            
    except GitHubAPIError as e:
        print(f"Error: {e}")