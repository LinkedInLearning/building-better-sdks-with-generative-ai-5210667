# Validating your Copilot SDK

This is the series of prompts we work through in validating your SDK. The "final" version is the last one but stepping through each is useful to understand the constraints and tradeoffs we make along the way.

# Validating Syntax

Does this code run?

Add it to our original prompt:

Reusing the existing GitHubAPi base class, please build a second class for interacting with the Issues endpoint. And please ensure the code runs

# Unit Tests

Can you generate the unit tests for this class?

Output: stargazer-tests.py