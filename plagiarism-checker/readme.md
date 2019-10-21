# Plagiarism Checker API

A simple plagiarism checker which uses natural language processing to compare two text files.

From: Python REST APIs with Flask, Docker, MongoDB, and AWS DevOps (a course on Udemy)

## Resource Table

| Resource          | Address   | Protocol | Params                  | Response + Status Code                                        |
|-------------------|-----------|----------|-------------------------|---------------------------------------------------------------|
| Register User     | /register | POST     | username, pwd           | 200 OK, 301 Invalid User                                      |
| Detect Similarity | /detect   | POST     | username, pwd, document | 200 OK, 301 Invalid User, 302 Unauthorized, 303 Out of tokens |
| Refill            | /refill   | POST     | username, admin_pwd     | 200 OK, 301 Invalid User, 304 Unauthorized Admin              |
