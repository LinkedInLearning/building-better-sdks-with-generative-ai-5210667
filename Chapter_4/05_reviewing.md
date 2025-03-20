# Validating your SDK

This is the series of prompts we work through in validating your SDK. Instead of using Claude to validate the Claude-generated SDK, we're going to use Claude to validate the final Copilot-generated SDK from the previous chapter. The "final" version of our prompt is the last one but stepping through each is useful to understand the constraints and tradeoffs we make along the way.

# Validating Syntax

How would flake8 or pylint rate the attached code?

Add it to our original prompt:

Reusing the existing GitHubAPi base class, please build a second class for interacting with the Issues endpoint. And please ensure the code runs

# Unit Tests

Can you generate the unit tests for this class?

Output: stargazer-tests.py