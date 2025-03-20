# Generating your SDK with another LLM

This is the series of prompts we work through in building your SDK using Claude. The "final" version is the last one but stepping through each is useful to understand the constraints and tradeoffs we make along the way.

# Attempt 1

Can you generate some functions to use the API described by this openapi spec?

# Attempt 2

Can you just generate the functions for just the stars and stargazing?

Output: stargazers.py

# Attempt 3

Can you just generate a Python class for the stars functionality and map the capabilities to methods? 

Output: Not what we want

# Attempt 4

Can you just generate a Python class using the OpenAPI specification for the stars functionality and map the capabilities to methods? 

Output: stargazers.py

# Attempt 5

Can you restructure this into a series of classes where there's a base GitHub API class that handles authentication, error handling, and retry logic and then a second class that extends or uses the first but just focused on the stars and stargazers functions?

Output: stargazers-advanced.py