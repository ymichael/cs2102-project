import sqlite3
import os
import schema


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
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()


def exec_schema_change(index, sql):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(sql)

    update_schema_table = """\
        INSERT INTO %s (id, sql_stmt)
            VALUES (?, ?)
    """ % SCHEMA_TABLE_NAME
    cursor.execute(update_schema_table, (index, sql))

    db.commit()
    db.close()
    print "Executed: (%s, %s)" % (index, sql)


def latest_schema():
    sql = "SELECT MAX(id) AS max FROM %s" % SCHEMA_TABLE_NAME
    db = connect_db()
    cursor = db.cursor()
    result = cursor.execute(sql).fetchone()
    db.close()
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
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    db.close()

    return [row['tbl_name'] for row in rows]


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
