# To change schema:
# 1. Add a new tuple to the end of the array in the form (<id>, <sql>).
# 2. Run db.update_schema() in a python shell.
SCHEMA = [
    (1, """\
        CREATE TABLE user (
            uid integer PRIMARY KEY,
            name varchar(255) NOT NULL,
            bio text,
            email varchar(255) NOT NULL,
            password_hash varchar(80) NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """),
    (2, """CREATE INDEX user_email ON user (email)"""),
    (3, """\
        CREATE TABLE listing (
            lid integer PRIMARY KEY,
            title varchar(255) NOT NULL,
            description text,
            owner_id integer NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES user(uid)
        )
    """),
    (4, """CREATE INDEX listing_owner ON listing (owner_id)"""),
    (5, """\
        CREATE TABLE category (
            cat_id integer PRIMARY KEY,
            label varchar(255) NOT NULL,
            description text
        )
    """),
    (6, """CREATE INDEX category_label ON category (label)"""),
    (7, """\
        CREATE TABLE listing_category (
            lid integer NOT NULL,
            cat_id integer NOT NULL,
            PRIMARY KEY(lid, cat_id),
            FOREIGN KEY(lid) REFERENCES listing(lid),
            FOREIGN KEY(cat_id) REFERENCES category(cat_id)
        )
    """),
    (8, """\
        CREATE TABLE comment (
            cid integer PRIMARY KEY,
            lid integer NOT NULL,
            uid integer NOT NULL,
            body text,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY(lid) REFERENCES listing(lid),
            FOREIGN KEY(uid) REFERENCES user(uid)
        )
    """),
    (9, """\
        CREATE VIRTUAL TABLE listing_search
            USING fts4(lid INT, content)
    """),
    (10, """\
        CREATE TRIGGER listing_search_insert
            AFTER INSERT ON listing
            BEGIN
                INSERT INTO listing_search(lid, content)
                    VALUES (new.lid, new.title || " " || new.description);
            END
    """),
    (11, """\
        CREATE TRIGGER listing_search_update
            AFTER UPDATE ON listing
            BEGIN
                UPDATE listing_search
                    SET content = new.title || " " || new.description
                    WHERE lid = new.lid;
            END
    """),
    (12, """\
        CREATE TRIGGER listing_search_delete
            AFTER DELETE ON listing
            BEGIN
                DELETE FROM listing_search
                    WHERE lid = old.lid;
            END
    """),

]
