import db


def listings(query, limit, offset=0):
    """Returns a list of listing_ids matching the query."""
    sql = """\
        SELECT listing_id FROM listing_search
            WHERE content MATCH ?
            LIMIT ? OFFSET ?"""
    with db.DatabaseCursor() as cursor:
        matching_listings = \
            cursor.execute(sql, (query, limit, offset)).fetchall()
    return [x['listing_id'] for x in matching_listings]


def all_listing_search_entries():
	sql = """SELECT * FROM listing_search"""
	with db.DatabaseCursor() as cursor:
		all_entries = cursor.execute(sql).fetchall()
	return all_entries