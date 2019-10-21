# modules required for app
from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["users"]

def UserExists(username):
    if users.find({"username": username}).count() == 0:
        return False
    else: 
        return True

def verifyPwd(username, pwd):
    hash_pwd = users.find(
        {
            'username' : username
        })[0]["password"]

    return bcrypt.checkpw(pwd.encode('utf8'), hash_pwd)

def countTokens(username):
    tokens = users.find(
        { 
            "username" : username 
        })[0]['tokens']

    return tokens

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]

        if UserExists(username):
            return { 
                "status": 301,
                "message": "This username is already "
            }
        
        hashed_pw = bcrypt.hashpw(postedData["password"].encode('utf8'), bcrypt.gensalt())
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "tokens"   : 6
        })

        return {
            "status" : 200,
            "message": "You have successfully signed up to the API with username {}.".format(username)
        }

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]
        
        if not UserExists(username):
            return {
                "status" : 301,
                "message": "Invalid username."
            }
        
        correctPwd = verifyPwd(username, postedData["password"])

        if not correctPwd:
            return {
                "status" : 302,
                "message": "Invalid password."
            }

        numTokens = countTokens(username)
        if numTokens <= 0:
            return {
                "status" : 303,
                "message": "Not enough tokens to perform transaciton."
            }, 303
        
        # Calculate the edit distance
        nlp = spacy.load('en_trf_bertbaseuncased_lg')
        
        text1 = nlp(text1)
        text2 = nlp(text2)

        # Get similarity ratio - ratio is a number between 0 and 1.  The closer to 1 
        # the more similar text1 and text2 are.
        ratio = text1.similarity(text2)

        currentTokens = countTokens(username)
        users.update({
            "username" : username            
        },{
            "$set":{
                "tokens" : currentTokens - 1
            }
        })

        return {
            "status"    : 200,
            "similarity": ratio,
            "message"   : "Similarity score calculated successfully."
        }

class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        refill_amt = postedData["refill"]

        if not UserExists(username):
            return {
                "status" : 301,
                "message": "Invalid username."
            }
        
        correctPwd = "abc123"

        if not postedData["admin_pwd"] == correctPwd:
            return {
                "status" : 304,
                "message": "Invalid admin password."
            }
        
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
        }

api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)