import db


def prepare(test):
    """Test decorator to initialize/clean up database."""
    def setup():
        db.init_db()

    def teardown():
        db.remove_db()

    test.setup = setup
    test.teardown = teardown
    return test
