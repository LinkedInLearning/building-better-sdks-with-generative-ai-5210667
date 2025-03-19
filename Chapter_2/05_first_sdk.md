# Generating your First SDK

This is the series of prompts we work through in building your SDK. The "final" version is the last one but stepping through each is useful to understand the constraints and tradeoffs we make along the way.

# Attempt 1

Can you generate some functions to use the API described by this openapi spec - https://raw.githubusercontent.com/github/rest-api-description/refs/heads/main/descriptions/ghec/ghec.2022-11-28.json ?

Output: first_sdk.py

# Attempt 2

Can you generate the functions to use the issues endpoint described by this openapi spec?

Or alternatively:

Can you just generate the functions for the issues?

Output: issues.py

# Attempt 3

Can you just generate the functions for all the endpoints and functionality in this Openapi doc?

Output: none

# Attempt 4

Can you just generate the functions for just the stars and stargazing?

Output: stargazers.py