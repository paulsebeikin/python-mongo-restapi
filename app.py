from flask import Flask, request

app = Flask(__name__)

@app.route('/') # index
def helloWorld():
    return "Hello World!!!"

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    # Get x,y from posted data
    dataDict = request.get_json()    
    # add x+y and store in z
    if "x" not in dataDict:
        return "[ERROR] : x is a required field", 400
    if "y" not in dataDict:
        return "[ERROR] : y is a required field", 400
    x = dataDict["x"]
    y = dataDict["y"]
    z = x + y
    # prepare a JSON object, in it "z" : z
    return {
        "z" : z
    }

# demonstrating JSON - arrays
@app.route('/users')
def getUsers():
    return {
        'Users': [
            {
                'FirstName' : 'Paul',
                'LastName' : 'Sebeikin',
                'Logon' : 'PaulS',
                'Admin' : 0
            },
            {        
                'FirstName' : 'Amy',
                'LastName' : 'Woolahan',
                'Logon' : 'AmyW',
                'Admin' : 1
            }
        ]
    }

@app.route('/test')
def test():
    name = 'Paul Sebeikin'
    age = 7*3
    json = {
        'Name'  : name,
        'Age'   : age,
        'Phones': [
            {
                "Phone Type"    : "Mobile",
                "Phone Number"  : 3231551
            },
            {
                "Phone Type"    : "Home",
                "Phone Number"  : 543342
            }
        ]    
    }

    return json

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)