from flask import Flask
import json
import os
from script import main
import asyncio

app = Flask(__name__)

def readFile(username):
    result = {}
    with open(f"./{username}.json","r") as f:
        result = json.load(f)
    return result

def writeFile(username, object):
    with open(f"./{username}.json", "w") as f:
        json.dump(object, f)
    return


@app.route("/<username>/<top>")
def home(username, top):
    top = int(top)

    result = {}
    
    if top == 100 and os.path.exists(f"./{username}.json"):
        print("Exist")
        result = readFile(username)
    elif top == 100 and os.path.exists(f"./{username}.json") == False:
        print("Does not Exist")

        result = asyncio.run(main(username, top))

        writeFile(username, result)
    else:
        print("Top is not 100")
        exist_object = readFile(username)
        result = asyncio.run(main(username, top))

        for key, value in result.items():
            exist_object[key] = value

        if top == 500:
            exist_object['fulfilled'] = 'true'
        
        writeFile(username, exist_object)
        
    for key, value in result.items():
        if key == 'fulfilled':
            result[key] = value
        else:
            result[key] = {
                "url_user": result[key]["url_user"],
                "username": result[key]["username"]
            }

    return result, 200

if __name__ == "__main__":
    app.run(debug=True)
