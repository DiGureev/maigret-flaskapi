from flask import Flask
import json
import os
from script import main
import asyncio

app = Flask(__name__)

@app.route("/<username>/<top>")
def home(username, top):
    top = int(top)
    
    if os.path.exists(f"./{username}{top}.json"):
        print("Exist")
        with open(f"./{username}{top}.json","r") as f:
            result = json.load(f)
    else:
        print("Does not Exist")
        result = asyncio.run(main(username, top))
        with open(f"./{username}{top}.json", "w") as f:
            json.dump(result, f)

    for key in result:
        result[key] = {
            "url_user": result[key]["url_user"],
            "username": result[key]["username"]
        }

    return result, 200

if __name__ == "__main__":
    app.run(debug=True)