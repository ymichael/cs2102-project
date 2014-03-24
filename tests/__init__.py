import nose

import db
import app

# Helpers
assert_eq = nose.tools.eq_

class TestController(object):
    def setup(self):
        self.app = app.app.test_client()
        self.db = db.connect_db()
        db.init()

    def teardown(self):
        self.db.close()
        db.remove()


def prepare(test):
    """Test decorator to initialize/clean up database."""
    def setup():
        db.init()

    def teardown():
        db.remove()

    test.setup = setup
    test.teardown = teardown
    return test
