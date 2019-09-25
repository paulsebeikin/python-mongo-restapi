from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
    if (functionName in ["add", "subtract", "multiply"]):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionName == 'divide'):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        # if i get here, then the resource Add was requested using the method POST

        # Step 1 : posted data
        postedData = request.get_json()
        
        # Step 2 : verify validity of posted data
        status_code = checkPostedData(postedData, "add")

        if (status_code != 200):
            return {
                "Message" : "And error happened.",
                "Status Code" : status_code
            }

        # if we get here then status code is 200
        
        # Step 3 : read in posted data variables and compute addition function
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x + y

        # Step 4 : return result
        return {
            'Message' : ret,
            'Status Code' : 200
        }

class Subtract(Resource):
    def post(self):
        # if i get here, then the resource Subtract was requested using the method POST

        # Step 1 : posted data
        postedData = request.get_json()
        
        # Step 2 : verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")

        if (status_code != 200):
            return {
                "Message" : "And error happened.",
                "Status Code" : status_code
            }

        # if we get here then status code is 200
        
        # Step 3 : read in posted data variables and compute subtraction function
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x - y

        # Step 4 : return result
        return {
            'Message' : ret,
            'Status Code' : 200
        }

class Divide(Resource):
    def post(self):
        # if i get here, then the resource Divide was requested using the method POST

        # Step 1 : posted data
        postedData = request.get_json()
        
        # Step 2 : verify validity of posted data
        status_code = checkPostedData(postedData, "divide")

        if (status_code != 200):
            return {
                "Message" : "And error happened.",
                "Status Code" : status_code
            }

        # if we get here then status code is 200
        
        # Step 3 : read in posted data variables and compute multiplication function
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = (x*1.0) / y

        # Step 4 : return result
        return {
            'Message' : ret,
            'Status Code' : 200
        }

class Multiply(Resource):
    def post(self):
        # if i get here, then the resource Multiply was requested using the method POST

        # Step 1 : posted data
        postedData = request.get_json()
        
        # Step 2 : verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")

        if (status_code != 200):
            return {
                "Message" : "And error happened.",
                "Status Code" : status_code
            }

        # if we get here then status code is 200
        
        # Step 3 : read in posted data variables and compute multiplication function
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x * y

        # Step 4 : return result
        return {
            'Message' : ret,
            'Status Code' : 200
        }

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")

@app.route('/') # index
def helloWorld():
    return "Hello World!!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)