import config
import db
import model
import flask
from flask import g, render_template, Flask, request, session, redirect
import json


app = Flask(__name__)
app.config.from_object(config.config())
app.secret_key = config.get_config('SECRET_KEY')


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


def login_user(uid):
    session['logged_in'] = True
    session['logged_in_user'] = uid


def is_logged_in():
    return session.get('logged_in')


def logout_user():
    session.pop('logged_in')
    session.pop('logged_in_user')


def generic_data_object():
    data = {}
    data['title'] = ''
    data.update(session)

    if data.get('logged_in'):
        data['user'] = model.user.get_user_info(data['logged_in_user'])

    return data


@app.route("/listings")
def listings():
    return json.dumps(model.listing.get_latest_listings(20))


@app.route("/tos")
def tos():
    # TODO(michael)
    return 'tos here'


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        data = generic_data_object()
        data['title'] = 'Sign Up'
        return render_template('signup.html', **data)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tos = request.form['tos']
        # TODO(michael): sanitize + validate.

        uid = model.user.create_new_user(name, email, password)
        login_user(uid)
        return redirect('/')


@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    uid = model.user.verify_login(email, password)
    if uid:
        login_user(uid)
        return redirect('/')
    else:
        # TODO(michael): Display some error message.
        return redirect('/')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/")
def index():
    data = generic_data_object()
    return render_template('index.html', **data)

if __name__ == "__main__":
    app.run()
