import db


def manage(test):
    def db_test_setup():
        db.init_db(True)

    test.setup = db_test_setup
    return test
