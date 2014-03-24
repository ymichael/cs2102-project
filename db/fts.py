import db

def init():
    populate_virtual_table()


def populate_virtual_table():
    # Populate fts table with existing data.
    sql = """\
        INSERT INTO listing_search(listing_id, content)
            SELECT id, title || " " || description
                FROM listings"""
    with db.DatabaseCursor() as cursor:
       cursor.execute(sql)