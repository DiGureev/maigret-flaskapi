from flask import Flask
from script import main
import asyncio

app = Flask(__name__)

@app.route("/<username>/<top>")
def home(username, top):
    top = int(top)
    result = asyncio.run(main(username, top))
    return result, 200

if __name__ == "__main__":
    app.run(debug=True)
