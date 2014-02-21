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
]
