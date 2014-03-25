import db
import model
import datetime

class Listing(model.base.BaseModel):
    properties = [
        'title',
        'description',
        'create_time',
        'last_update_time',
    ]

    def __init__(self, listing_id=None):
        self.id = listing_id

    def check_is_saved(self):
        return self.id

    def get(self):
        return get_listing_info(self.id)

    @property
    def owner_id(self):
        return self.get_prop('owner_id')

    @owner_id.setter
    def owner_id(self, val):
        if not self.check_is_saved():
            # Listings are not transferrable. So only allow setting if not
            # created yet.
            self.set_prop('owner_id', val)

    def validate(self):
        # TODO(michael): Refactor, code duplication from model/user.
        return (self.title and self.description and self.owner_id)

    def put(self):
        update_existing_listing(
            self.id, self.title, self.description)
        return self.id

    def post(self):
        new_listing_id = create_new_listing(
            self.title, self.description, self.owner_id)
        self.id = new_listing_id
        return new_listing_id

    def delete(self):
        delete_listing(self.id)


def delete_listing(listing_id):
    sql = """DELETE FROM listings WHERE lid = ?"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (listing_id,))


def update_existing_listing(listing_id, title, description):
    sql = """\
        UPDATE listings
        SET title = ?, description = ?, last_update_time = ?
        WHERE lid = ?"""
    with db.DatabaseCursor() as cursor:
        now = datetime.datetime.now()
        cursor.execute(sql, (title, description, now, listing_id))


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
    sql = """\
        SELECT *
            FROM listings
            WHERE lid = ?"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql, (listing_id,)).fetchone()
    return obj


def get_listings_info(listing_ids):
    sql = """\
        SELECT *
            FROM listings l, users u, (
                SELECT l.lid, COUNT(c.cid) AS comment_count
                    FROM listings l
                        LEFT JOIN comments c
                            ON l.lid = c.lid
                    GROUP BY l.lid) c
            WHERE l.lid IN (%s) AND
                c.lid = l.lid AND
                l.owner_id = u.uid
        """ % ','.join('?' * len(listing_ids))
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql, listing_ids).fetchall()
    return rows


def get_listings_for_user(uid):
    sql = """\
        SELECT *
            FROM listings l, users u, (
                SELECT l.lid, COUNT(c.cid) AS comment_count
                    FROM listings l
                        LEFT JOIN comments c
                            ON l.lid = c.lid
                    GROUP BY l.lid) c
            WHERE l.owner_id = u.uid AND
                c.lid = l.lid AND
                l.owner_id = ?
            ORDER BY l.lid DESC"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(
            sql, (uid,)).fetchall()
    return obj


def get_related_listings(listing_id, limit, offset=0):
    # TODO(michael): tmp implementation.
    sql = """\
        SELECT *
            FROM listings l, users u, (
                SELECT l.lid, COUNT(c.cid) AS comment_count
                    FROM listings l
                        LEFT JOIN comments c
                            ON l.lid = c.lid
                    GROUP BY l.lid) c
            WHERE l.owner_id = u.uid AND
                c.lid = l.lid AND
                l.owner_id = (
                    SELECT owner_id FROM listings
                        WHERE lid = ?) AND
                l.lid <> ?
            ORDER BY l.lid DESC
            LIMIT ? OFFSET ?"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(
            sql, (listing_id, listing_id, limit, offset)).fetchall()
    return obj


def get_lids_by_cat_ids(cat_ids, limit, offset=0):
    sql = """\
        SELECT l.lid
            FROM listings l, listing_categories c
            WHERE l.lid = c.lid AND
                c.cat_id IN (%s)
            ORDER BY l.lid DESC
            LIMIT ? OFFSET ?
        """ % ','.join('?' * len(cat_ids))
    with db.DatabaseCursor() as cursor:
        cat_ids.extend([limit, offset])
        obj = cursor.execute(sql, cat_ids).fetchall()
    return [x['lid'] for x in obj]


def get_number_of_listings_in_cat_ids(cat_ids):
    sql = """\
        SELECT COUNT(*) as count
            FROM listings l, listing_categories c
            WHERE l.lid = c.lid AND
                c.cat_id IN (%s)
        """ % ','.join('?' * len(cat_ids))
    with db.DatabaseCursor() as cursor:
        row = cursor.execute(sql, cat_ids).fetchone()
    return row['count']


def get_latest_listings(limit, offset=0):
    sql = """\
        SELECT *
            FROM listings l, users u, (
                SELECT l.lid, COUNT(c.cid) AS comment_count
                    FROM listings l
                        LEFT JOIN comments c
                            ON l.lid = c.lid
                    GROUP BY l.lid) c
            WHERE l.owner_id = u.uid AND
                c.lid = l.lid
            ORDER BY l.lid DESC
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
