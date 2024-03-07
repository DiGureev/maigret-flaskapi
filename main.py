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

    result_object = {
                "sites": {}
            }
    
    if top == 100 and os.path.exists(f"./{username}.json"):
        print("Exist")
        result_object = readFile(username)
    elif top == 100 and os.path.exists(f"./{username}.json") == False:
        print("Does not Exist")

        result_object["sites"] = asyncio.run(main(username, top))

        writeFile(username, result_object)
    else:
        print("Top is not 100")
        exist_object = readFile(username)

        result_object["sites"]  = asyncio.run(main(username, top))

        for key, value in result_object["sites"].items():
            exist_object["sites"][key] = value

        if top == 500:
            exist_object["fulfilled"] = "true"
        
        writeFile(username, exist_object)
        
    for key, value in result_object["sites"].items():
        result_object["sites"][key] = {
            "url_user": result_object["sites"][key]["url_user"],
            "username": result_object["sites"][key]["username"]
        }

    return result_object, 200

if __name__ == "__main__":
    app.run(debug=True)
