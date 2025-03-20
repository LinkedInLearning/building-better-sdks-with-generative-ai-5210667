import requests
import json
from typing import Dict, List, Optional, Union, Any
from datetime import datetime


class StargazersClient:
    """
    A client for interacting with the Stargazers API.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize a new Stargazers API client.
        
        Args:
            base_url: The base URL for the Stargazers API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def list_stargazers(self, 
                      repository_id: str,
                      limit: Optional[int] = None, 
                      offset: Optional[int] = None,
                      sort_by: Optional[str] = None) -> Dict[str, Any]:
        """
        List all stargazers for a specific repository with optional pagination.
        
        Args:
            repository_id: The unique identifier of the repository
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort_by: Field to sort by (e.g., "starred_at", "username")
            
        Returns:
            Dictionary containing stargazer data and pagination info
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort_by is not None:
            params['sort_by'] = sort_by
            
        response = self.session.get(f"{self.base_url}/repositories/{repository_id}/stargazers", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_stargazer(self, repository_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get details for a specific stargazer of a repository.
        
        Args:
            repository_id: The unique identifier of the repository
            user_id: The unique identifier of the user
            
        Returns:
            Dictionary containing stargazer details
        """
        response = self.session.get(f"{self.base_url}/repositories/{repository_id}/stargazers/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def add_stargazer(self, repository_id: str, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a user as a stargazer to a repository.
        
        Args:
            repository_id: The unique identifier of the repository
            user_id: The unique identifier of the user
            metadata: Optional additional metadata about the star action
            
        Returns:
            Dictionary containing the created stargazer record
        """
        data = {
            "user_id": user_id,
            "starred_at": datetime.utcnow().isoformat()
        }
        
        if metadata:
            data["metadata"] = metadata
            
        response = self.session.post(f"{self.base_url}/repositories/{repository_id}/stargazers", json=data)
        response.raise_for_status()
        return response.json()
    
    def remove_stargazer(self, repository_id: str, user_id: str) -> None:
        """
        Remove a user as a stargazer from a repository.
        
        Args:
            repository_id: The unique identifier of the repository
            user_id: The unique identifier of the user
        """
        response = self.session.delete(f"{self.base_url}/repositories/{repository_id}/stargazers/{user_id}")
        response.raise_for_status()
    
    def get_stargazer_count(self, repository_id: str) -> int:
        """
        Get the total count of stargazers for a repository.
        
        Args:
            repository_id: The unique identifier of the repository
            
        Returns:
            Integer count of stargazers
        """
        response = self.session.get(f"{self.base_url}/repositories/{repository_id}/stargazers/count")
        response.raise_for_status()
        return response.json().get("count", 0)
    
    def list_user_starred_repositories(self, 
                                     user_id: str,
                                     limit: Optional[int] = None, 
                                     offset: Optional[int] = None,
                                     sort_by: Optional[str] = None) -> Dict[str, Any]:
        """
        List all repositories starred by a specific user with optional pagination.
        
        Args:
            user_id: The unique identifier of the user
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort_by: Field to sort by (e.g., "starred_at", "repository_name")
            
        Returns:
            Dictionary containing repository data and pagination info
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort_by is not None:
            params['sort_by'] = sort_by
            
        response = self.session.get(f"{self.base_url}/users/{user_id}/starred", params=params)
        response.raise_for_status()
        return response.json()
    
    def is_repository_starred(self, repository_id: str, user_id: str) -> bool:
        """
        Check if a user has starred a specific repository.
        
        Args:
            repository_id: The unique identifier of the repository
            user_id: The unique identifier of the user
            
        Returns:
            Boolean indicating whether the repository is starred by the user
        """
        try:
            response = self.session.get(f"{self.base_url}/repositories/{repository_id}/stargazers/{user_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False
            raise
    
    def get_star_history(self, repository_id: str, 
                        interval: str = "day",
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get historical data of star counts for a repository over time.
        
        Args:
            repository_id: The unique identifier of the repository
            interval: Time interval for grouping (day, week, month, year)
            start_date: Optional start date for the history period (ISO format)
            end_date: Optional end date for the history period (ISO format)
            
        Returns:
            Dictionary containing historical star count data
        """
        params = {"interval": interval}
        
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        response = self.session.get(f"{self.base_url}/repositories/{repository_id}/star-history", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_top_stargazers(self, limit: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Get users who have starred the most repositories.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of dictionaries containing user information and star counts
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
            
        response = self.session.get(f"{self.base_url}/stargazers/top", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_trending_repositories(self, 
                                period: str = "day",
                                category: Optional[str] = None,
                                language: Optional[str] = None,
                                limit: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Get repositories that are trending based on star activity.
        
        Args:
            period: Time period for trend calculation (day, week, month)
            category: Optional category filter
            language: Optional programming language filter
            limit: Maximum number of repositories to return
            
        Returns:
            List of dictionaries containing repository information and star metrics
        """
        params = {"period": period}
        
        if category:
            params["category"] = category
        if language:
            params["language"] = language
        if limit is not None:
            params["limit"] = limit
            
        response = self.session.get(f"{self.base_url}/repositories/trending", params=params)
        response.raise_for_status()
        return response.json()
    
    def export_stargazers(self, repository_id: str, format: str = "json") -> bytes:
        """
        Export the list of stargazers for a repository in the specified format.
        
        Args:
            repository_id: The unique identifier of the repository
            format: Export format (json, csv, xml)
            
        Returns:
            Bytes containing the exported data
        """
        params = {"format": format}
        
        response = self.session.get(
            f"{self.base_url}/repositories/{repository_id}/stargazers/export", 
            params=params,
            headers={"Accept": f"application/{format}"}
        )
        response.raise_for_status()
        return response.content


# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = StargazersClient("https://api.example.com/v1", api_key="your_api_key")
    
    # List stargazers for a repository
    repo_id = "example/repository"
    stargazers = client.list_stargazers(repo_id, limit=20, sort_by="starred_at")
    print(f"Repository has {len(stargazers['data'])} recent stargazers")
    
    # Get stargazer count
    count = client.get_stargazer_count(repo_id)
    print(f"Total stargazer count: {count}")
    
    # Add a new stargazer
    new_stargazer = client.add_stargazer(repo_id, "user123", metadata={"referrer": "homepage"})
    print(f"Added stargazer: {new_stargazer['username']}")
    
    # Check if a user has starred a repository
    is_starred = client.is_repository_starred(repo_id, "user456")
    print(f"Repository is starred by user456: {is_starred}")
    
    # Get star history
    history = client.get_star_history(repo_id, interval="week", start_date="2023-01-01")
    print(f"Retrieved star history with {len(history['data'])} data points")
    
    # Get trending repositories
    trending = client.get_trending_repositories(period="week", language="python", limit=5)
    print(f"Top trending Python repositories this week:")
    for repo in trending:
        print(f"- {repo['name']}: {repo['new_stars']} new stars")