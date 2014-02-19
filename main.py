import db
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    users = db.users()
    return "%s world!" % users[0]

if __name__ == "__main__":
    app.run()
