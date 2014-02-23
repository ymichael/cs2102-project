import db
import model

class Listing(object):
    def __init__(self, listing_id=None):
        self.listing_id = listing_id

    def info(self):
        if hasattr(self, '_info'):
            return self._info

        if self.listing_id:
            self._info = get_listing_info(self.listing_id) or {}
        else:
            self._info = {}

        return self._info

    def get_title(self):
        return self.info().get('title')

    def set_title(self, value):
        self.info()['title'] = value

    title = property(get_title, set_title)

    def get_description(self):
        return self.info().get('description')

    def set_description(self, value):
        self.info()['description'] = value

    description = property(get_description, set_description)

    def get_owner_id(self):
        return self.info().get('owner_id')

    def set_owner_id(self, value):
        if not self.listing_id:
            # Listings are not trasferrable. So only allow setting if not
            # created yet.
            self.info()['owner_id'] = value

    owner_id = property(get_owner_id, set_owner_id)

    def validate(self):
        # TODO(michael): Refactor, code duplication from model/user.
        return (self.title and self.description and self.owner_id)

    def save(self):
        if not self.validate():
            raise Exception('Trying to save invalid user.',
                            self.title, self.description, self.owner_id)

        if self.listing_id:
            update_existing_listing(
                self.listing_id, self.title, self.description)
        else:
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
