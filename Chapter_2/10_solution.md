# Solution: Improve your OpenAPI specification

Looking at the ngrok OpenAPI specification 
https://raw.githubusercontent.com/ngrok/ngrok-openapi/refs/heads/main/ngrok.yaml

Here are some fixes that probably apply to yours too:

- Add security schemas to specify how to authenticate with the API
- Include example values for both requests and responses
- Use components to define data structures once
- Include metadata for where users can find support, additional information, and more