import db
from flask import Flask
app = Flask(__name__)

db.init()

@app.route("/")
def hello():
    test = db.test()
    return "%s world!" % test[0]

if __name__ == "__main__":
    app.run()
