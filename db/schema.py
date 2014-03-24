# To change schema:
# 1. Add a new tuple to the end of the array in the form (<id>, <sql>).
# 2. Run db.update_schema() in a python shell.
SCHEMA = [
    (1, """\
        CREATE TABLE users (
            uid integer PRIMARY KEY,
            name varchar(255) NOT NULL,
            bio text,
            email varchar(255) NOT NULL,
            password_hash varchar(80) NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """),
    (2, """CREATE INDEX users_email ON users (email)"""),
    (3, """\
        CREATE TABLE listings (
            lid integer PRIMARY KEY,
            title varchar(255) NOT NULL,
            description text,
            owner_id integer NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """),
    (4, """CREATE INDEX listings_owner ON listings (owner_id)"""),
    (5, """\
        CREATE TABLE category (
            cat_id integer PRIMARY KEY,
            label varchar(255) NOT NULL,
            description text
        )
    """),
    (6, """\
        CREATE TABLE listing_categories (
            lid integer NOT NULL,
            cat_id integer NOT NULL,
            is_main integer,
            PRIMARY KEY(lid, cat_id)
        )
    """),
    (7, """\
        CREATE TABLE comments (
            cid integer PRIMARY KEY,
            lid integer NOT NULL,
            uid integer NOT NULL,
            body text,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """),
    (8, """\
        CREATE TABLE hearts (
            uid integer NOT NULL,
            lid integer NOT NULL,
            PRIMARY KEY(uid, lid)
        )
    """),
    (9, """\
        CREATE TABLE flags (
            uid integer NOT NULL,
            lid integer NOT NULL,
            PRIMARY KEY(uid, lid)
        )
    """),
    (10, """\
        CREATE TABLE followers (
            follower_id integer NOT NULL,
            following_id integer NOT NULL,
            PRIMARY KEY(follower_id, following_id)
        )
    """),
    (11, """\
        CREATE VIRTUAL TABLE listing_search
            USING fts4(lid INT, content)
    """),
    (12, """\
        CREATE TRIGGER listing_search_insert
            AFTER INSERT ON listings
            BEGIN
                INSERT INTO listing_search(lid, content)
                    VALUES (new.lid, new.title || " " || new.description);
            END
    """),
    (13, """\
        CREATE TRIGGER listing_search_update
            AFTER UPDATE ON listings
            BEGIN
                UPDATE listing_search
                    SET content = new.title || " " || new.description
                    WHERE lid = new.lid;
            END
    """),
    (14, """\
        CREATE TRIGGER listing_search_delete
            AFTER DELETE ON listings
            BEGIN
                DELETE FROM listing_search
                    WHERE lid = old.lid;
            END
    """),

]
