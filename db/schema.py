# To change schema:
# 1. Add a new tuple to the end of the array in the form (<id>, <sql>).
# 2. Run db.update_schema() in a python shell.
SCHEMA = [
    (1, """\
        CREATE TABLE test (
             id int,
             tmp text
       )
    """),
    (2, "DROP TABLE test"),
    (3, """\
        CREATE TABLE users (
            id integer PRIMARY KEY,
            name varchar(255),
            first_name varchar(50),
            last_name varchar(50),
            email varchar(255) NOT NULL,
            password_hash varchar(80) NOT NULL
        )
    """),
]
