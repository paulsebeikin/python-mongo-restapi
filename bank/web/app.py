from flask import Flask, request
from pymongo import MongoClient
from flask_restful import Api, Resource
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.Bank
users = db["users"]

def UserExists(username):
    if users.count({"username": username}) == 0:
        return False
    else: 
        return True

def verifyPwd(username, password):
    if not UserExists(username):
        return False
    
    hash_pwd = users.find(
        {
            'username' : username
        })[0]["password"]

    return bcrypt.checkpw(password.encode('utf8'), hash_pwd)

def balance(username):
    balance = users.find({
        "username" : username
    })[0]["balance"]

    return balance

def debt(username):
    debt = users.find({
        "username" : username
    })[0]["debt"]

    return debt

def generateReturnDictionary(status, message):
    return {
        "status" : status,
        "message": message
    }, status

def verifyCredentials(username, password):
    if not UserExists(username):
        return generateReturnDictionary(301, "Invalid Username."), True
    
    correct_pwd = verifyPwd(username, password)

    if not correct_pwd:
        return generateReturnDictionary(302, "Unauthorized"), True

    return None, False

def updateBalance(username, amt):
    users.update({
        "username" : username
    }, {
        "$set": {
            "balance" : amt
        }
    })

def updateDebt(username, amt):
    users.update({
        "username" : username
    }, {
        "$set": {
            "debt" : amt
        }
    })

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]

        if UserExists(username):
            return generateReturnDictionary(301, "This username is already taken.")
        
        hashed_pw = bcrypt.hashpw(postedData["password"].encode('utf8'), bcrypt.gensalt())
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "balance"  : 0,
            "debt"     : 0           
        })

        return generateReturnDictionary(200, "You have successfully signed up to the API with username {}.".format(username))

class Deposit(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        amt = postedData["amt"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        if (amt<0):
            return generateReturnDictionary(305, "Amount entered must be >= 0.")

        bal = balance(username)
        bal_bank = balance('BANK')
        
        updateBalance(username, bal + amt - 1) # bank fee charged
        updateBalance('BANK', bal_bank + 1)

        new_bal = balance(username)
        
        return generateReturnDictionary(200, "Transaction successful.  Balance was R{}. Balance is now R{}".format(bal, new_bal))

class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        to_acct = postedData["to"]
        amt = postedData["amt"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        if (amt<0):
            return generateReturnDictionary(304, "Amount entered must be >= 0.")

        if not UserExists(to_acct):
            return generateReturnDictionary(301, "Invalid Username.")

        bal = balance(username)        

        if (amt > bal):
            return generateReturnDictionary(303, "Not Enough Funds.")
        
        to_bal = balance(to_acct)
        bank_bal = balance('BANK')

        updateBalance('BANK', bank_bal + 1) # bank transaction fee
        updateBalance(username, bal - amt)
        updateBalance(to_acct, to_bal + amt - 1)

        return generateReturnDictionary(200, "Successfully tranferred R{} to account {}".format(amt, to_acct))

class Balance(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        bal = balance(username)

        retJson = users.find({
            "username": username
        },{
            "password": 0,
            "_id": 0
        })[0]

        return retJson, 200

class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        amt = postedData["amt"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        if (amt<0):
            return generateReturnDictionary(305, "Amount entered must be >= 0.")

        dbt = debt(username)
        bal = balance(username)

        updateBalance(username, bal + amt)

        updateDebt(username, dbt + amt)

        return generateReturnDictionary(200, "User {} has taken out a new loan to the value of R{}".format(username, amt))

class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        amt = postedData["amt"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        if (amt<0):
            return generateReturnDictionary(305, "Amount entered must be >= 0.")        

        dbt = debt(username)
        bal = balance(username)

        if (amt > bal):
            return generateReturnDictionary(303, "Not Enough Funds.")

        updateBalance(username, bal - amt)
        updateDebt(username, dbt - amt)

        return generateReturnDictionary(200, "User {} has successfully paid off a loan to the value of R{}".format(username, amt))

api.add_resource(Register, "/register")
api.add_resource(Deposit, "/deposit")
api.add_resource(Transfer, "/transfer")
api.add_resource(Balance, "/balance")
api.add_resource(TakeLoan, "/takeloan")
api.add_resource(PayLoan, "/payloan")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)