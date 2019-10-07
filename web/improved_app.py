from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase # collection
users = db["users"]

class Register(Resource):
    def post(self):

        # Step 1 - get posted data (username and pwd)
        postedData = request.get_json()  

        username = postedData["username"]       

        hash_password = bcrypt.hashpw(postedData["password"].encode('utf8'), bcrypt.gensalt())

        # Step 2 - update the database
        users.insert({
            'username': username,
            'password': hash_password,
            'sentence': '',
            'tokens': 10
        })

        # Step 3 - return status
        return {
            'Message' : "You successfully signed up for the API",
            'Status Code' : 200
        }

class Store(Resource):
    def post(self):

        # Step 1 - get posted data (username and pwd)
        postedData = request.get_json()  

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # Step 2 - verify username and password
        user_authorized = verifyPwd(username, password)

        if not user_authorized:
            return {
                'Message' : 'Incorrect username or password.',
                'Status'  : 302
            }

        # Step 3 - verify tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            return {
                'Message' : 'Not enough tokens to complete transaction.',
                'Status'  : 301
            }   

        # Step 4 - deduct token and store sentence
        users.update(
            {
                'username' : username
            },
            {"$set" : {
                'sentence' : sentence,
                'tokens' : num_tokens - 1
            }}
        )

        # Step 5 - return success
        return {
            'Message' : 'Successfully stored sentence and token deducted.',
            'Status'  : 200
        }

class Retrieve(Resource):
    def post(self):
        # Step 1 - get posted data (username and pwd)
        postedData = request.get_json()  

        username = postedData["username"]
        password = postedData["password"]

        # Step 2 - verify username and password
        user_authorized = verifyPwd(username, password)

        if not user_authorized:
            return {
                'Message' : 'Incorrect username or password.',
                'Status'  : 302
            }

        # Step 3 - verify tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            return {
                'Message' : 'Not enough tokens to retrieve sentence.',
                'Status'  : 301
            }   

        # Step 4 - retrieve sentence
        sentence = users.find({
            'username' : username
        })[0]['sentence']

        # Step 5 - deduct token and store sentence
        users.update(
            {
                'username' : username
            },
            {"$set" : {                
                'tokens' : num_tokens - 1
            }}
        )

        # Step 6 - return success
        return {
            'Sentence' : sentence,
            'Status'  : 200
        }

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


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Retrieve, "/get")

@app.route('/') # index
def improved_api():
    return "This is the improved API index text."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)