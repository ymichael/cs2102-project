# To change schema:
# 1. Add a new tuple to the end of the array in the form (<id>, <sql>).
# 2. Run db.update_schema() in a python shell.
SCHEMA = [
    (1, """\
        CREATE TABLE users (
            id integer PRIMARY KEY,
            name varchar(255) NOT NULL,
            email varchar(255) NOT NULL,
            password_hash varchar(80) NOT NULL
        )
    """),
    (2, """CREATE INDEX users_email ON users (email)"""),
    (3, """\
        CREATE TABLE listings (
            id integer PRIMARY KEY,
            title varchar(255) NOT NULL,
            description text,
            owner_id integer NOT NULL
        )
    """),
    (4, """CREATE INDEX listings_owner ON listings (owner_id)"""),
]
