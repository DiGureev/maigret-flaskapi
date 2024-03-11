from flask import Flask
import json
import os
from script import main
import asyncio

app = Flask(__name__)

@app.route('/favicon.ico')
def checkFav():
    return {}, 200


@app.route("/<username>/<top>")
def home(username, top):
    top = int(top)

    existObject = {}
    result = {}
    
    if os.path.exists(f"./{username}.json"):
        print("Exist")
        with open(f"./{username}.json","r") as f:
            existObject = json.load(f)
        
        result = asyncio.run(main(username, top))
        for key in result:
            result[key] = {
                "url_user": result[key]["url_user"],
                "username": result[key]["username"]
            }
        
        for key, value in result.items():
            existObject[key] = value
        
        with open(f"./{username}.json", "w") as f:
            json.dump(existObject, f)
        
    else:
        print("Does not Exist")
        result = asyncio.run(main(username, top))

        for key in result:
            result[key] = {
                "url_user": result[key]["url_user"],
                "username": result[key]["username"]
            }
        
        with open(f"./{username}.json", "w") as f:
            json.dump(result, f)

    return result, 200

@app.route('/all/<name>')
def getResult(name):
    result = {}

    if os.path.exists(f"./{name}.json"):
        print("Exist")
        with open(f"./{name}.json","r") as f:
            result = json.load(f)
    
    return result, 200


if __name__ == "__main__":
    app.run(debug=True)