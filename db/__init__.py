import sqlite3
import os
import schema


def _execute_query(sql, db=None, commit=False):
    database = db or connect_db()
    ret = database.cursor().execute(sql).fetchall()

    if commit:
        database.commit()

    if db:
        database.close()

    return ret


def connect_db():
    db = sqlite3.connect("dev.sqlite")
    # This allows us to treat rows as python dictionaries instead of tuples.
    db.row_factory = sqlite3.Row
    return db


SCHEMA_TABLE_NAME = 'schema_table'
def maybe_init_schema():
    if SCHEMA_TABLE_NAME not in list_tables():
        sql = """\
            CREATE TABLE %s (
                id int UNSIGNED PRIMARY KEY,
                sql_stmt text NOT NULL
            )
        """ % SCHEMA_TABLE_NAME
        _execute_query(sql, commit=True)


def exec_schema_change(index, sql):
    _execute_query(sql, commit=True)
    print "Executed: (%s, %s)" % (index, sql)

    update_schema_table = """\
        INSERT INTO %s (id, sql_stmt)
            VALUES (%s, "%s")
    """ % (SCHEMA_TABLE_NAME, index, sql)
    _execute_query(update_schema_table, commit=True)


def latest_schema():
    sql = "SELECT MAX(id) FROM %s" % SCHEMA_TABLE_NAME
    try:
        return int(_execute_query(sql)[0][0])
    except:
        return 0


def list_tables():
    sql = """\
        SELECT *
        FROM sqlite_master
        WHERE type = 'table'
    """
    return [row['tbl_name'] for row in _execute_query(sql)]


def check_schema():
    """Checks that the schema is up-to-date."""
    latest_executed_schema = latest_schema()

    max_index = latest_executed_schema
    for index, sql in schema.SCHEMA:
        if index > latest_executed_schema:
            max_index = index

    if max_index != latest_executed_schema:
        print "SCHEMA NOT UP-TO-DATE, UPDATE SCHEMA."

def update_schema():
    latest_executed_schema = latest_schema()

    for index, sql in schema.SCHEMA:
        if index > latest_executed_schema:
            exec_schema_change(index, sql)

def init_db():
    maybe_init_schema()
    check_schema()
