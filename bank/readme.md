# Bank API
An API that mimics a banking system.  The system should allow users to register for the API, deposit money into the account, transfer money into another account, check the balance of their account, take out a loan and pay off a loan.

## Resource Table

| Resource          | Address   | Protocol | Params                         | Response + Status Code                                                                      |
|-------------------|-----------|----------|--------------------------------|---------------------------------------------------------------------------------------------|
| Register User     | /register | POST     | username, pwd                  | 200 OK, 301 Invalid User                                                                    |
| Deposit money     | /deposit  | POST     | username, pwd, amt             | 200 OK, 301 Invalid User, 302 Unauthorized                                                  |
| Transfer money    | /transfer | POST     | username, pwd, to_account, amt | 200 OK, 301 Invalid User, 302 Unauthorized, 303 Not Enough Funds                            |
| Check Balance     | /balance  | POST     | username, pwd                  | 200 OK, 301 Invalid User, 302 Unauthorized, 304 Amount Less than Zero                       |
| Take loan         | /takeloan | POST     | username, pwd, amt             | 200 OK, 301 Invalid User, 302 Unauthorized, 304 Amount Less than Zero                       |
| Pay loan          | /payloan  | POST     | username, pwd, amt             | 200 OK, 301 Invalid User, 302 Unauthorized, 303 Not Enough Funds, 304 Amount Less than Zero |