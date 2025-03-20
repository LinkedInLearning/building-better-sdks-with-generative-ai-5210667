"""
This file contains mock test data for use in the GitHubStarsClient unit tests.
These objects represent the type of responses you might get from the GitHub API.
"""

# Mock response for repository information
MOCK_REPO_INFO = {
    "id": 12345678,
    "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY3OA==",
    "name": "hello-world",
    "full_name": "octocat/hello-world",
    "private": False,
    "owner": {
        "login": "octocat",
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "type": "User",
        "site_admin": False
    },
    "html_url": "https://github.com/octocat/hello-world",
    "description": "This is a sample repository",
    "fork": False,
    "url": "https://api.github.com/repos/octocat/hello-world",
    "created_at": "2011-01-26T19:01:12Z",
    "updated_at": "2021-07-28T23:28:06Z",
    "pushed_at": "2021-07-28T23:28:03Z",
    "homepage": "https://github.com",
    "size": 108,
    "stargazers_count": 1524,
    "watchers_count": 1524,
    "language": "Python",
    "forks_count": 1162,
    "open_issues_count": 130,
    "license": {
        "key": "mit",
        "name": "MIT License",
        "url": "https://api.github.com/licenses/mit"
    },
    "topics": [
        "octocat",
        "api",
        "github"
    ],
    "default_branch": "main",
    "network_count": 1162,
    "subscribers_count": 1662
}

# Mock response for listing stargazers
MOCK_STARGAZERS = [
    {
        "login": "user1",
        "id": 1001,
        "node_id": "MDQ6VXNlcjEwMDE=",
        "avatar_url": "https://avatars.githubusercontent.com/u/1001?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/user1",
        "html_url": "https://github.com/user1",
        "type": "User",
        "site_admin": False
    },
    {
        "login": "user2",
        "id": 1002,
        "node_id": "MDQ6VXNlcjEwMDI=",
        "avatar_url": "https://avatars.githubusercontent.com/u/1002?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/user2",
        "html_url": "https://github.com/user2",
        "type": "User",
        "site_admin": False
    },
    {
        "login": "user3",
        "id": 1003,
        "node_id": "MDQ6VXNlcjEwMDM=",
        "avatar_url": "https://avatars.githubusercontent.com/u/1003?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/user3",
        "html_url": "https://github.com/user3",
        "type": "User",
        "site_admin": False
    }
]

# Mock response for listing stargazers with timestamps
MOCK_STARGAZERS_WITH_TIMESTAMPS = [
    {
        "starred_at": "2020-01-01T10:00:00Z",
        "user": {
            "login": "user1",
            "id": 1001,
            "node_id": "MDQ6VXNlcjEwMDE=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1001?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/user1",
            "html_url": "https://github.com/user1",
            "type": "User",
            "site_admin": False
        }
    },
    {
        "starred_at": "2020-02-15T14:30:45Z",
        "user": {
            "login": "user2",
            "id": 1002,
            "node_id": "MDQ6VXNlcjEwMDI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1002?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/user2",
            "html_url": "https://github.com/user2",
            "type": "User",
            "site_admin": False
        }
    },
    {
        "starred_at": "2020-03-20T09:15:30Z",
        "user": {
            "login": "user3",
            "id": 1003,
            "node_id": "MDQ6VXNlcjEwMDM=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1003?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/user3",
            "html_url": "https://github.com/user3",
            "type": "User",
            "site_admin": False
        }
    }
]

# Mock response for listing starred repositories
MOCK_STARRED_REPOS = [
    {
        "id": 23456789,
        "node_id": "MDEwOlJlcG9zaXRvcnkyMzQ1Njc4OQ==",
        "name": "repo1",
        "full_name": "user1/repo1",
        "private": False,
        "owner": {
            "login": "user1",
            "id": 1001,
            "node_id": "MDQ6VXNlcjEwMDE=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1001?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/user1",
            "html_url": "https://github.com/user1",
            "type": "User",
            "site_admin": False
        },
        "html_url": "https://github.com/user1/repo1",
        "description": "A sample repository",
        "fork": False,
        "url": "https://api.github.com/repos/user1/repo1",
        "created_at": "2019-01-15T20:30:45Z",
        "updated_at": "2021-06-10T15:20:30Z",
        "pushed_at": "2021-06-10T15:20:27Z",
        "stargazers_count": 345,
        "watchers_count": 345,
        "language": "JavaScript",
        "forks_count": 123,
        "open_issues_count": 10,
        "license": {
            "key": "mit",
            "name": "MIT License",
            "url": "https://api.github.com/licenses/mit"
        },
        "topics": ["api", "javascript", "library"]
    },
    {
        "id": 34567890,
        "node_id": "MDEwOlJlcG9zaXRvcnkzNDU2Nzg5MA==",
        "name": "repo2",
        "full_name": "user2/repo2",
        "private": False,
        "owner": {
            "login": "user2",
            "id": 1002,
            "node_id": "MDQ6VXNlcjEwMDI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1002?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/user2",
            "html_url": "https://github.com/user2",
            "type": "User",
            "site_admin": False
        },
        "html_url": "https://github.com/user2/repo2",
        "description": "Another sample repository",
        "fork": False,
        "url": "https://api.github.com/repos/user2/repo2",
        "created_at": "2018-11-20T10:15:30Z",
        "updated_at": "2021-05-25T09:45:15Z",
        "pushed_at": "2021-05-25T09:45:12Z",
        "stargazers_count": 567,
        "watchers_count": 567,
        "language": "Python",
        "forks_count": 234,
        "open_issues_count": 25,
        "license": {
            "key": "apache-2.0",
            "name": "Apache License 2.0",
            "url": "https://api.github.com/licenses/apache-2.0"
        },
        "topics": ["api", "python", "framework"]
    }
]

# Mock response for trending repositories
MOCK_TRENDING_REPOS = [
    {
        "author": "user1",
        "name": "trending-repo1",
        "full_name": "user1/trending-repo1",
        "avatar": "https://github.com/user1.png",
        "url": "https://github.com/user1/trending-repo1",
        "description": "A trending repository example",
        "language": "Python",
        "languageColor": "#3572A5",
        "stars": 1200,
        "forks": 150,
        "currentPeriodStars": 300,
        "builtBy": [
            {
                "username": "contributor1",
                "href": "https://github.com/contributor1",
                "avatar": "https://github.com/contributor1.png"
            },
            {
                "username": "contributor2",
                "href": "https://github.com/contributor2",
                "avatar": "https://github.com/contributor2.png"
            }
        ]
    },
    {
        "author": "user2",
        "name": "trending-repo2",
        "full_name": "user2/trending-repo2",
        "avatar": "https://github.com/user2.png",
        "url": "https://github.com/user2/trending-repo2",
        "description": "Another trending repository example",
        "language": "JavaScript",
        "languageColor": "#f1e05a",
        "stars": 980,
        "forks": 120,
        "currentPeriodStars": 250,
        "builtBy": [
            {
                "username": "contributor3",
                "href": "https://github.com/contributor3",
                "avatar": "https://github.com/contributor3.png"
            },
            {
                "username": "contributor4",
                "href": "https://github.com/contributor4",
                "avatar": "https://github.com/contributor4.png"
            }
        ]
    }
]

# Mock response for repository recommendations
MOCK_RECOMMENDATIONS = [
    {
        "id": 45678901,
        "node_id": "MDEwOlJlcG9zaXRvcnk0NTY3ODkwMQ==",
        "name": "recommended-repo1",
        "full_name": "org1/recommended-repo1",
        "private": False,
        "owner": {
            "login": "org1",
            "id": 5001,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjUwMDE=",
            "avatar_url": "https://avatars.githubusercontent.com/u/5001?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/org1",
            "html_url": "https://github.com/org1",
            "type": "Organization",
            "site_admin": False
        },
        "html_url": "https://github.com/org1/recommended-repo1",
        "description": "A recommended repository",
        "fork": False,
        "url": "https://api.github.com/repos/org1/recommended-repo1",
        "created_at": "2020-02-10T14:25:30Z",
        "updated_at": "2021-07-15T11:30:45Z",
        "pushed_at": "2021-07-15T11:30:40Z",
        "stargazers_count": 789,
        "watchers_count": 789,
        "language": "TypeScript",
        "forks_count": 345,
        "open_issues_count": 15,
        "license": {
            "key": "mit",
            "name": "MIT License",
            "url": "https://api.github.com/licenses/mit"
        },
        "topics": ["web", "typescript", "frontend"],
        "recommendation_reason": "Based on repositories you've starred"
    },
    {
        "id": 56789012,
        "node_id": "MDEwOlJlcG9zaXRvcnk1Njc4OTAxMg==",
        "name": "recommended-repo2",
        "full_name": "org2/recommended-repo2",
        "private": False,
        "owner": {
            "login": "org2",
            "id": 5002,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjUwMDI=",