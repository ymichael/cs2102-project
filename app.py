import config
import db
import model
import flask
import json
import functools
import datetime

from flask import g
from flask import render_template
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import flash

app = Flask(__name__)
app.config.from_object(config.config())
app.secret_key = config.get_config('SECRET_KEY')

# Jinja filter
def format_datetime(value):
    dt = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%d %B, %H:%M")
app.jinja_env.filters['datetime'] = format_datetime


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
    session['logged_in_uid'] = uid


def logged_in_user():
    return session['logged_in_uid']


def is_logged_in():
    return session.get('logged_in')


def logout_user():
    session.pop('logged_in')
    session.pop('logged_in_uid')


def login_required(route):
    @functools.wraps(route)
    def new_route(*args, **kwargs):
        if not is_logged_in():
            return 'Unauhorized', 401
        return route(*args, **kwargs)
    return new_route


def generic_data_object():
    data = {}
    data['title'] = ''
    data['q'] = ''
    data.update(session)
    if data.get('logged_in'):
        data['logged_in_user'] = model.user.get_user_info(data['logged_in_uid'])
    return data


@app.route("/listing/new", methods=['POST'])
@login_required
def listing_new():
    title = request.form.get('title')
    description = request.form.get('description')
    # TODO(michael): Sanitize + validate

    new_listing = model.listing.Listing()
    new_listing.owner_id = logged_in_user()
    new_listing.title = title
    new_listing.description = description
    new_listing.save()

    # Comma separated
    categories = request.form.get('categories')
    categories = categories.split(',')

    for cat in categories:
        cat_id = model.category.create_or_retrieve_category(cat)
        model.category.add_listing_to_category(new_listing.id, cat_id)

    # Redirect to newly created listing's page.
    return redirect('/listing/%s' % new_listing.id)


@app.route("/listing/<int:listing_id>")
def listing(listing_id):
    data = generic_data_object()
    data['title'] = 'Listing'
    data['listing'] = model.listing.Listing(listing_id).info()
    data['owner'] = model.user.get_user_info(data['listing']['owner_id'])
    data['categories'] = model.category.listing_categories(listing_id)
    data['related_listings'] = model.listing.get_related_listings(listing_id, 10)
    data['comments'] = model.comment.get_comments_for_listing(listing_id, time_ordered=False)
    return render_template('listing.html', **data)


@app.route("/listing/<int:listing_id>/comment", methods=['POST'])
@login_required
def listing_comment_new(listing_id):
    body = request.form.get('comment')
    # TODO(michael): Sanitize + validate

    new_comment = model.comment.Comment()
    new_comment.body = body
    new_comment.uid = logged_in_user()
    new_comment.lid = listing_id
    new_comment.save()

    # Redirect to listing's page.
    return redirect('/listing/%s' % listing_id)


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
        categories = model.category.listing_categories(listing_id)
        data['categories'] = ', '.join([x['label'] for x in categories])
        return render_template('listing_edit.html', **data)
    else:
        if not 'update' in request.form:
            # Use clicked delete.
            listing = model.listing.Listing(listing_id)
            listing.delete()
            flash("Listing deleted.", "info")
            return redirect('/')

        title = request.form['title']
        description = request.form['description']
        # TODO(michael): Sanitize + validate

        new_listing = model.listing.Listing(listing_id)
        new_listing.title = title
        new_listing.description = description
        new_listing.save()

        # Update categories
        categories = request.form.get('categories')
        categories = [x.upper() for x in categories.split(',')]
        old_categories = model.category.listing_categories(listing_id)
        for old_cat in old_categories:
            if old_cat['label'] not in categories:
                model.category.remove_listing_from_category(listing_id, old_cat['cat_id'])
            else:
                categories.remove(old_cat['label'])

        for cat in categories:
            cat_id = model.category.create_or_retrieve_category(cat)
            model.category.add_listing_to_category(new_listing.id, cat_id)

        # Redirect to newly updated listing's page.
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
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        tos = request.form.get('tos')
        # TODO(michael): sanitize + validate.

        if not tos:
            flash("Sorry, you need to agree to our terms of service in order to\
                create an account.", "error")
            return redirect('/signup')

        uid = model.user.create_new_user(name, email, password)
        login_user(uid)
        return redirect('/')


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    uid = model.user.verify_login(email, password)
    if uid:
        login_user(uid)
        flash("Welcome back!", "info")
        return redirect('/')
    else:
        flash("Invalid login credentials.", "error")
        return redirect('/')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/search")
def search():
    results_per_page = 20
    query = request.args.get('q')
    page = request.args.get('p') or 1
    page = int(page)

    data = generic_data_object()
    data['q'] = query
    data['p'] = page
    data['total_results'] = model.search.listings_count(query)
    data['max_p'] = int(round(float(data['total_results']) / 20 + 0.5))
    listings = model.listing.get_listings_info(
        model.search.listings(
            query, results_per_page,
            (page - 1) * results_per_page))
    # TODO(michael): Super inefficient.
    for l in listings:
        l['categories'] = model.category.listing_categories(l['lid'])
    data['results'] = listings
    return render_template('search.html', **data)


@app.route("/user/<int:uid>/edit", methods=['GET', 'POST'])
@login_required
def user_edit(uid):
    if logged_in_user() != uid:
        return redirect('/user/%s' % uid)

    if request.method == 'GET':
        data = generic_data_object()
        data['user'] = model.user.get_user_info(uid)
        if not data['user']:
            return 'No such user', 404
        return render_template('user_edit.html', **data)
    else:
        name = request.form.get('name')
        bio = request.form.get('bio')
        old_password = request.form.get('old_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')
        # TODO(michael): sanitize + validate.
        user = model.user.User(uid)

        if (old_password or new_password1 or new_password2) and \
                not (old_password and new_password1 and new_password2):
            flash("Sorry, you need to fill in all three password fields to\
                change your password", "error")
            return redirect('/user/%s/edit' % uid)

            if new_password1 != new_password2:
                flash("Sorry, your new passwords do not match.", "error")
                return redirect('/user/%s/edit' % uid)

            # Verify old password.
            uid = model.user.verify_login(user.email, password)
            if not uid:
                flash("Sorry, your old password is incorrect.", "error")
                return redirect('/user/%s/edit' % uid)

            # Change password.
            model.user.update_password(uid, new_password1)
            flash("Password changed.", "info")
        
        user.name = name
        user.bio = bio
        user.save()
        flash("Profile updated.", "info")

        return redirect('/user/%s/edit' % uid)


@app.route("/user/<int:uid>")
def user(uid):
    data = generic_data_object()
    data['user'] = model.user.get_user_info(uid)
    if not data['user']:
        return 'No such user', 404

    data['listings'] = model.listing.get_listings_for_user(uid)
    return render_template('user.html', **data)


@app.route("/")
def index():
    data = generic_data_object()
    listings = model.listing.get_latest_listings(20)
    # TODO(michael): Super inefficient.
    for l in listings:
        l['categories'] = model.category.listing_categories(l['lid'])
    data['listings'] = listings
    return render_template('index.html', **data)


def main():
    # Initialize db/fts
    db.init()
    db.fts.init()
    db.mock_data.maybe_bootstrap_db()
    model.category.init()
    app.run()


if __name__ == "__main__":
    main()
