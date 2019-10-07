# Improved API - User Sentence Service

## Requirements

1. Registration of a user (starts off with zero tokens).
2. Each user gets 10 tokens.
3. Store a sentence on our database for 1 token.
4. Retreive his stored sentence on our database for 1 token.

Other topics covered:
 - Password hashing and salting.

## Resource Table

| Resource          | Address   | Protocol | Params                  | Response + Status Code                    |
|-------------------|-----------|----------|-------------------------|-------------------------------------------|
| Register User     | /register | POST     | username, pwd           | 200 OK                                    |
| Store Sentence    | /store    | POST     | username, pwd, sentence | 200 OK 301 Out of Tokens 302 Unauthorized |
| Retrieve Sentence | /get      | GET      | username, pwd           | 200 OK 301 Out of Tokens 302 Unauthorized |


