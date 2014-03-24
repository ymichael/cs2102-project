import db
import model


CATEGORIES = [
    'ART',
    'BOOKS',
    'ELECTRONICS',
    'FOOD',
    'HOME & LIVING',
    'HOUSING',
    'JEWELLERY',
    'KIDS',
    'MEN',
    'VINTAGE',
    'WEDDINGS',
    'WOMEN',
]


class Category(model.base.BaseModel):
    properties = ['label', 'desription']

    def __init__(self, cat_id=None):
        self.id = cat_id

    def check_is_saved(self):
        return self.id

    def get(self):
        return get_category_info(self.id)

    def validate(self):
        return self.label

    def post(self):
        new_cat_id = create_category(self.label)
        self.id = new_cat_id
        return new_cat_id


def init():
    """Inserts various categories into the categories table."""
    # TODO(michael): Make less flaky.
    if get_number_of_categories() != len(CATEGORIES):
        for cat in CATEGORIES:
            create_category(cat)


def create_category(cat_label):
    sql = """\
        INSERT INTO category (label)
            VALUES (?)"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (cat_label,))
        new_id = cursor.lastrowid
    return new_id


def get_category_info(cat_id):
    sql = """\
        SELECT * FROM category WHERE cat_id = ?"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql, (cat_id,)).fetchone()
    return obj


def get_number_of_categories():
    sql = """\
        SELECT COUNT(*) AS count FROM category"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql).fetchone()
    return obj['count']


def get_all_cat_ids():
    sql = """\
        SELECT cat_id FROM category"""
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql).fetchall()
    return [x['cat_id'] for x in rows]


def add_listing_to_category(lid, cat_id):
    sql = """\
        INSERT INTO listing_categories (lid, cat_id)
            VALUES (?, ?)"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (lid, cat_id))


def remove_listing_from_category(lid, cat_id):
    sql = """\
        DELETE FROM listing_categories
            WHERE lid = ? AND
            cat_id = ?"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (lid, cat_id))


def listing_categories(lid):
    sql = """\
        SELECT c.cat_id, c.label
            FROM listing_categories l, category c
            WHERE l.lid = ? AND
                l.cat_id = c.cat_id"""
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql, (lid,)).fetchall()
    return rows


def cat_ids_to_labels(cat_ids):
    sql = """\
        SELECT label
            FROM category
            WHERE cat_id IN (%s)
        """ % ','.join('?' * len(cat_ids))
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql, cat_ids).fetchall()
    return [x['label'] for x in rows]


def number_of_listing_categories():
    sql = """\
        SELECT COUNT(*) as count FROM listing_categories"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql).fetchone()
    return obj['count']