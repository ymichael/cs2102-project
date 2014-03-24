import db
import model

class Comment(model.base.BaseModel):
    properties = [
        'body',
        'uid',
        'lid',
        'create_time',
    ]

    def __init__(self, comment_id=None):
        self.id = comment_id

    def check_is_saved(self):
        return self.id

    def get(self):
        return get_comment_info(self.id)

    def validate(self):
        # TODO(michael): Refactor, code duplication from model/user.
        return (self.uid and self.lid and self.body)

    def post(self):
        new_cid = create_new_comment(self.body, self.uid, self.lid)
        self.id = new_cid
        return new_cid


def get_comment_info(comment_id):
    sql = """\
        SELECT *
            FROM comments
            WHERE cid = ?"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql, (comment_id,)).fetchone()
    return obj


def create_new_comment(body, uid, lid):
    # Check that uid exists.
    if not model.user.get_user_info(uid):
        raise Exception('No such user.')

    # Check that listing exists.
    if not model.listing.get_listing_info(lid):
        raise Exception('No such listing.')

    sql = """\
        INSERT INTO comments (body, uid, lid)
            VALUES (?, ?, ?)"""

    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (body, uid, lid))
        new_id = cursor.lastrowid
    return new_id


def get_comments_for_listing(lid, time_ordered=True):
    sql = """\
        SELECT *
            FROM listings l, comments c, users u
            WHERE l.lid = c.lid AND
                l.lid = ? AND
                c.uid = u.uid"""
    if not time_ordered:
        sql += " ORDER BY cid DESC"
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql, (lid,)).fetchall()
    return rows


def get_number_of_comments():
    sql = """\
        SELECT COUNT(*) AS count FROM comments"""
    with db.DatabaseCursor() as cursor:
        row = cursor.execute(sql).fetchone()
    return row['count']