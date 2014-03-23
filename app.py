import config
import db
import model
import flask
from flask import g, render_template, Flask, request, session, redirect
import json
import functools


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


def logged_in_user():
    return session['logged_in_user']


def is_logged_in():
    return session.get('logged_in')


def logout_user():
    session.pop('logged_in')
    session.pop('logged_in_user')


def login_required(route):
    @functools.wraps(route)
    def new_route(*args, **kwargs):
        if not is_logged_in():
            return redirect('/')
        return route(*args, **kwargs)
    return new_route


def generic_data_object():
    data = {}
    data['title'] = ''
    data.update(session)
    if data.get('logged_in'):
        data['user'] = model.user.get_user_info(data['logged_in_user'])
    return data


@app.route("/listing/new", methods=['GET', 'POST'])
@login_required
def listing_new():
    if request.method == 'GET':
        data = generic_data_object()
        data['title'] = 'New Listing'
        return render_template('listing_new.html', **data)
    else:
        title = request.form['title']
        description = request.form['description']
        # TODO(michael): Sanitize + validate

        new_listing = model.listing.Listing()
        new_listing.owner_id = logged_in_user()
        new_listing.title = title
        new_listing.description = description
        new_listing.save()

        # Redirect to newly created listing's page.
        return redirect('/listing/%s' % new_listing.id)


@app.route("/listing/<int:listing_id>")
def listing(listing_id):
    data = generic_data_object()
    data['title'] = 'Listing'
    data['listing'] = model.listing.Listing(listing_id).info()

    print data
    return render_template('listing.html', **data)


@app.route("/listing/<int:listing_id>/edit", methods=['GET', 'POST'])
@login_required
def listing_edit(listing_id):
    listing = model.listing.Listing(listing_id)
    if logged_in_user() != listing.owner_id:
        return redirect('/listing/%s', listing_id)

    if request.method == 'GET':
        data = generic_data_object()
        data['title'] = 'Listing'
        data['listing'] = listing.info()
        return render_template('listing_edit.html', **data)
    else:
        title = request.form['title']
        description = request.form['description']
        # TODO(michael): Sanitize + validate

        new_listing = model.listing.Listing(listing_id)
        new_listing.title = title
        new_listing.description = description
        new_listing.save()

        # Redirect to newly created listing's page.
        return redirect('/listing/%s' % new_listing.id)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if is_logged_in():
        return redirect('/')

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
