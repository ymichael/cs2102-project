import sqlite3
import os
import config
import schema
import mock_data
import fts


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    db = sqlite3.connect(config.get_config('DATABASE'))
    # This allows us to treat rows as python dictionaries instead of tuples.
    db.row_factory = dict_factory
    return db


class DatabaseCursor(object):
    def __enter__(self):
        self.db = connect_db()
        return self.db.cursor()

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()


SCHEMA_TABLE_NAME = 'schema_table'
def maybe_init_schema():
    if SCHEMA_TABLE_NAME not in list_tables():
        sql = """\
            CREATE TABLE %s (
                id int UNSIGNED PRIMARY KEY,
                sql_stmt text NOT NULL
            )
        """ % SCHEMA_TABLE_NAME

        with DatabaseCursor() as cursor:
            cursor.execute(sql)


def exec_schema_change(index, sql):
    update_schema_table = """\
        INSERT INTO %s (id, sql_stmt)
            VALUES (?, ?)
    """ % SCHEMA_TABLE_NAME

    with DatabaseCursor() as cursor:
        cursor.execute(sql)
        cursor.execute(update_schema_table, (index, sql))

    if config.get_config('DEBUG'):
        print "Executed: (%s, %s)" % (index, sql)


def latest_schema():
    maybe_init_schema()
    sql = "SELECT MAX(id) AS max FROM %s" % SCHEMA_TABLE_NAME

    with DatabaseCursor() as cursor:
        result = cursor.execute(sql).fetchone()

    try:
        return int(result['max'])
    except:
        return 0


def list_tables():
    sql = """\
        SELECT s.tbl_name
        FROM sqlite_master AS s
        WHERE type = 'table'
    """
    with DatabaseCursor() as cursor:
        rows = cursor.execute(sql).fetchall()

    return [row['tbl_name'] for row in rows]


def check_schema():
    """Checks that the schema is up-to-date.

    Returns boolean based on whether schema is up-to-date.
    """
    latest_executed_schema = latest_schema()

    max_index = latest_executed_schema
    for index, sql in schema.SCHEMA:
        max_index = max(max_index, index)

    if max_index != latest_executed_schema:
        if config.get_config('DEBUG'):
            print "SCHEMA NOT UP-TO-DATE, UPDATE SCHEMA."
        return False

    return True


def update_schema():
    latest_executed_schema = latest_schema()

    for index, sql in schema.SCHEMA:
        if index > latest_executed_schema:
            exec_schema_change(index, sql)


def remove():
    try:
        os.remove(config.get_config('DATABASE'))
    except:
        pass


def init():
    """Initialize DB.

    If clean is True, removes existing database and starts from scratch.
    Used in tests.
    """
    if config.get_config('TESTING'):
        remove()

    maybe_init_schema()
    check_schema()

    # TODO(michael): tmp. for dev.
    # Just forcibly update the schema everytime.
    update_schema()
