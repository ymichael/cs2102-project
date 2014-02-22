import db
import flask


g = flask.g
render_template = flask.render_template


app = flask.Flask(__name__)

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
def index():
    data = {
        'title': 'hello',
        'text': 'world',
    }
    return render_template('index.html', **data)

if __name__ == "__main__":
    app.run()
