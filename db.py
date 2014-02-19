import sqlite3

db = sqlite3.connect(":memory:")

queries_run_once = [
    """\
    CREATE TABLE test (
        val varchar(255)
    )""",
    "INSERT INTO test (val) VALUES ('Hello')"
]

test_query = "SELECT * FROM test"

def init():
    cursor = db.cursor()
    for q in queries_run_once:
        cursor.execute(q)
        db.commit()

def test():
    cursor = db.cursor()
    cursor.execute(test_query)
    return cursor.fetchall()

def main():
    init()
    print users()

if __name__ == '__main__':
    main()

