from flask import Flask, request
from pymongo import MongoClient
import requests
from flask_restful import Api, Resource
import bcrypt
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["users"]

def UserExists(username):
    if users.find({"username": username}).count() == 0:
        return False
    else: 
        return True

def countTokens(username):
    tokens = users.find(
        { 
            "username" : username 
        })[0]['tokens']

    return tokens

def verifyCredentials(username, password):
    if not UserExists(username):
        return generateReturnDictionary(301, "Invalid Username."), True
    
    correct_pwd = verifyPwd(username, password)

    if not correct_pwd:
        return generateReturnDictionary(302, "Invalid Password"), True

    return None, False

def verifyPwd(username, password):
    if not UserExists(username):
        return False
    
    hash_pwd = users.find(
        {
            'username' : username
        })[0]["password"]

    return bcrypt.checkpw(password.encode('utf8'), hash_pwd)

def generateReturnDictionary(status, message):
    return {
        "status" : status,
        "message": message
    }

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]

        if UserExists(username):
            return { 
                "status": 301,
                "message": "This username is already taken."
            }, 301
        
        hashed_pw = bcrypt.hashpw(postedData["password"].encode('utf8'), bcrypt.gensalt())
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "tokens"   : 6
        })

        return {
            "status" : 200,
            "message": "You have successfully signed up to the API with username {}.".format(username)
        }, 200

class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        url = postedData["url"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson

        tokens = users.find({
            "username" : username  
        }[0]["tokens"])

        if tokens <= 0:
            return generateReturnDictionary(303, "Not enough tokens.")

        r = requests.get(url)
        retJson = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen('python classify_image.py --models_dir=. --image_file=./temp.jpg')
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                retJson = json.load(g)
        
        # remove a token from the user
        users.update({
            "username": username
        }, {
            "$set": {
                "tokens" : tokens - 1
            }
        })

        return retJson
        

class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        refill_amt = postedData["refill"]

        retJson, error = verifyCredentials(username, postedData["password"])

        if error:
            return retJson
        
        correctPwd = "abc123"

        if not postedData["admin_pwd"] == correctPwd:
            return {
                "status" : 304,
                "message": "Invalid admin password."
            }, 304
        
        currentTokens = countTokens(username)
        users.update({
            "username" : username
        },{
            "$set":{
                "tokens" : refill_amt
            }
        })

        return {
            "status" : 200,
            "message": "Tokens refilled.  New token count: {}.".format(refill_amt)
        }, 200

api.add_resource(Register, "/register")
api.add_resource(Classify, "/classify")
api.add_resource(Refill, "/refill")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)