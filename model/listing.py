import db
import model

class Listing(model.base.BaseModel):
    properties = ['title', 'description']

    def __init__(self, listing_id=None):
        print 'qwer'
        self.listing_id = listing_id

    def check_is_saved(self):
        return self.listing_id

    def get(self):
        return get_listing_info(self.listing_id)

    @property
    def owner_id(self):
        return self.get_prop('owner_id')

    @owner_id.setter
    def owner_id(self, val):
        if not self.listing_id:
            # Listings are not transferrable. So only allow setting if not
            # created yet.
            self.set_prop('owner_id', val)

    def validate(self):
        # TODO(michael): Refactor, code duplication from model/user.
        print self.owner_id
        return (self.title and self.description and self.owner_id)

    def put(self):
        update_existing_listing(
            self.listing_id, self.title, self.description)
        return self.listing_id

    def post(self):
        new_listing_id = create_new_listing(
            self.title, self.description, self.owner_id)
        self.listing_id = new_listing_id
        return new_listing_id


def update_existing_listing(listing_id, title, description):
    sql = """\
        UPDATE listings
        SET title = ?, description = ?
        WHERE id = ?"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (title, description, listing_id))


def create_new_listing(title, description, owner_id):
    # Check that owner_id exists.
    if not model.user.get_user_info(owner_id):
        raise Exception('No such user.')

    sql = """\
        INSERT INTO listings (title, description, owner_id)
            VALUES (?, ?, ?)"""

    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (title, description, owner_id))
        new_id = cursor.lastrowid
    return new_id


def get_listing_info(listing_id):
    sql = "SELECT * FROM listings WHERE id = ?"
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql, (listing_id,)).fetchone()
    return obj


def get_latest_listings(limit, offset=0):
    sql = """\
        SELECT * FROM listings AS l
        ORDER BY l.id DESC
        LIMIT ? OFFSET ?"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql, (limit, offset)).fetchall()
    return obj


def get_all_listings():
    sql = "SELECT * FROM listings"
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql).fetchall()
    return obj


def get_number_of_listings():
    sql = "SELECT COUNT(*) as count FROM listings"
    with db.DatabaseCursor() as cursor:
        row = cursor.execute(sql).fetchone()
    return row['count']