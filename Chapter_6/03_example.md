# Improving your OpenAPI Specification

## Write better descriptions

/users:
  get:
    summary: "Get users"


/users:
  get:
    summary: "Retrieve a list of users"
    description: "Returns a paginated list of users ordered by creation date. Supports filtering by username."
    parameters:
      - name: "username"
        in: "query"
        description: "Filter users by username"
        required: false
        schema:
          type: "string"

## Don't forget your error responses

responses:
  '200':
    description: "Success"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '400':
    description: "Bad request - invalid parameters"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
  '401':
    description: "Unauthorized - invalid or missing token"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
  '500':
    description: "Internal server error"
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'

## Prepare for change

/users:
  get:
    parameters:
      - name: "limit"
        in: "query"
        schema:
          type: integer
/posts:
  get:
    parameters:
      - name: "limit"
        in: "query"
        schema:
          type: integer


components:
  parameters:
    LimitParam:
      name: "limit"
      in: "query"
      description: "Number of items to return"
      required: false
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 10
paths:
  /users:
    get:
      parameters:
        - $ref: '#/components/parameters/LimitParam'
  /posts:
    get:
      parameters:
        - $ref: '#/components/parameters/LimitParam'

## Include examples

schema:
  type: object
  properties:
    id:
      type: integer
    name:
      type: string


schema:
  type: object
  properties:
    id:
      type: integer
      example: 42
    name:
      type: string
      example: "Alice"
  example:
    id: 42
    name: "Alice"

## Don't get ahead of the specification

The calue of the specification is it's predictability, standardization, and common patterns.