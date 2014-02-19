import sqlite3


def connect_db():
    db = sqlite3.connect("dev.sqlite")
    # This allows us to treat rows as python dictionaries instead of tuples.
    db.row_factory = sqlite3.Row
    return db


def close_db(error):
    """Closes the database again at the end of the request."""


def init_db():
    db = connect_db()
    with open('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def list_tables():
    db = connect_db()
    sql = """\
        SELECT *
        FROM sqlite_master
        WHERE type = 'table'
    """
    print db.cursor().execute(sql).fetchall()
