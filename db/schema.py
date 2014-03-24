# To change schema:
# 1. Add a new tuple to the end of the array in the form (<id>, <sql>).
# 2. Run db.update_schema() in a python shell.
SCHEMA = [
    (1, """\
        CREATE TABLE users (
            id integer PRIMARY KEY,
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
            id integer PRIMARY KEY,
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
            id integer PRIMARY KEY,
            label varchar(255) NOT NULL,
            description text
        )
    """),
    (6, """\
        CREATE TABLE listing_categories (
            listing_id integer NOT NULL,
            category_id integer NOT NULL,
            is_main integer,
            PRIMARY KEY(listing_id, category_id)
        )
    """),
    (7, """\
        CREATE TABLE comments (
            id integer PRIMARY KEY,
            listing_id integer NOT NULL,
            author_id integer NOT NULL,
            body text,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """),
    (8, """\
        CREATE TABLE hearts (
            user_id integer NOT NULL,
            listing_id integer NOT NULL,
            PRIMARY KEY(user_id, listing_id)
        )
    """),
    (9, """\
        CREATE TABLE flags (
            flagger_id integer NOT NULL,
            listing_id integer NOT NULL,
            PRIMARY KEY(flagger_id, listing_id)
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
            USING fts4(listing_id INT, content)
    """),
    (12, """\
        CREATE TRIGGER listing_search_insert
            AFTER INSERT ON listings
            BEGIN
                INSERT INTO listing_search(listing_id, content)
                    VALUES (new.id, new.title || " " || new.description);
            END
    """),
    (13, """\
        CREATE TRIGGER listing_search_update
            AFTER UPDATE ON listings
            BEGIN
                UPDATE listing_search
                    SET content = new.title || " " || new.description
                    WHERE listing_id = new.id;
            END
    """),
    (14, """\
        CREATE TRIGGER listing_search_delete
            AFTER DELETE ON listings
            BEGIN
                DELETE FROM listing_search
                    WHERE listing_id = old.id;
            END
    """),

]
