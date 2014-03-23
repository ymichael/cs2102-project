import config
import db
import model
import flask
from flask import g, render_template, Flask
import json


app = Flask(__name__)
app.config.from_object(config.config())


# Initialize db.
db.init_db()
# db.mock_data.maybe_bootstrap_db()


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


@app.route("/listings")
def listings():
    return json.dumps(model.listing.get_latest_listings(20))


@app.route("/")
def index():
    data = {
        'title': 'hello',
        'text': 'world',
    }
    return render_template('index.html', **data)

if __name__ == "__main__":
    app.run()
