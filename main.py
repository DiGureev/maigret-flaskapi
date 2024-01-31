from flask import Flask, jsonify
from script import main
import asyncio

app = Flask(__name__)

@app.route("/<username>")
def home(username):
    result = asyncio.run(main(username))
    return result, 200

if __name__ == "__main__":
    app.run(debug=True)
