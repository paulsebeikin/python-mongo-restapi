# Image-Recognition API

A simple image recognition API that accepts an image and tries to classify as a type of object using a percentage of certainty.

From: Python REST APIs with Flask, Docker, MongoDB, and AWS DevOps (a course on Udemy)

## Resource Table

| Resource          | Address   | Protocol | Params                       | Response + Status Code                                        |
|-------------------|-----------|----------|------------------------------|---------------------------------------------------------------|
| Register User     | /register | POST     | username, pwd                | 200 OK, 301 Invalid User                                      |
| Classify Image    | /classify | POST     | username, pwd, url~          | 200 OK, 301 Invalid User, 302 Unauthorized, 303 Out of tokens |
| Refill            | /refill   | POST     | username, admin_pwd, refill  | 200 OK, 301 Invalid User, 304 Unauthorized Admin              |

~ : points to image on the Internet.