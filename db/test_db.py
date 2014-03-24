from tests import assert_eq
import tests
import db
import schema

class TestDb(tests.TestController):
    def setup(self):
        super(TestDb, self).setup()
        self.latest = 0
        for idx, sql in schema.SCHEMA:
            self.latest = max(self.latest, idx)

    def test_list_tables(self):
        assert 'schema_table' in db.list_tables()

        db.remove()
        assert_eq(db.list_tables(), [])

    def test_latest_schema(self):
        assert_eq(db.latest_schema(), self.latest)
        db.remove()
        assert_eq(db.latest_schema(), 0)

    def test_check_schema(self):
        db.remove()
        if self.latest != 0:
            assert not db.check_schema()

        db.update_schema()
        assert db.check_schema()
