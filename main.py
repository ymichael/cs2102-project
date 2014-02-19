import db
from flask import Flask, g


app = Flask(__name__)


# Debug mode
# TODO(michael): Set this using env variables.
app.debug = True


# Initialize db.
db.init_db()


def get_db():
    """Opens a new database connection if there is none yet for the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = db.connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/")
def hello():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO test (val) VALUES ('Hello')")
    db.commit()

    cursor.execute("SELECT * FROM test")
    test = cursor.fetchone()['val']

    return "%s World!" % test

if __name__ == "__main__":
    app.run()
