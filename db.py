import sqlite3

db = sqlite3.connect(":memory:")

queries_run_once = ["""\
    CREATE TABLE users (
        name varchar(255)
    )""",
    "INSERT INTO users (name) VALUES ('Hello')"
]

test_query = "SELECT * FROM users"


def users():
    cursor = db.cursor()

    for q in queries_run_once:
        cursor.execute(q)
        db.commit()

    cursor.execute(test_query)
    return cursor.fetchall()


def main():
    print users()

if __name__ == '__main__':
    main()

