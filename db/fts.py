import db

def init():
    maybe_populate_virtual_table()


def has_created():
    sql = """\
        SELECT COUNT(*) AS count FROM listing_search"""
    with db.DatabaseCursor() as cursor:
        obj = cursor.execute(sql).fetchone()
    return obj['count'] != 0


def maybe_populate_virtual_table():
    if has_created():
        return

    # Populate fts table with existing data.
    sql = """\
        INSERT INTO listing_search(lid, content)
            SELECT lid, title || " " || description
                FROM listing"""
    with db.DatabaseCursor() as cursor:
       cursor.execute(sql)