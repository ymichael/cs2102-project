import db
import hashlib
import random

class User(object):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def info(self):
        if hasattr(self, '_info'):
            return self._info

        if self.user_id:
            self._info = get_user_info(self.user_id) or {}
            return self._info

        return {}

    def get_name(self):
        return self.info().get('name')

    def set_name(self, value):
        self.info()['name'] = value

    name = property(get_name, set_name)

    def get_email(self):
        return self.info().get('email')

    def set_email(self, value):
        self.info()['email'] = value

    email = property(get_email, set_email)

    def validate(self):
        # TODO(michael): Add validation
        return (self.name and self.email and self.user_id)

    def save(self):
        if not self.validate():
            raise Exception('Trying to save invalid user.')
        update_existing_user(self.user_id, self.name, self.email)


def update_existing_user(user_id, name, email):
    sql = """\
        UPDATE users
        SET name = ?, email = ?
        WHERE id = ?"""
    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (name, email, user_id))


def create_new_user(name, email, password):
    password_hash = get_password_hash(password)
    sql = """\
        INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)"""

    with db.DatabaseCursor() as cursor:
        cursor.execute(sql, (name, email, password_hash))
        new_user_id = cursor.lastrowid

    return new_user_id


def get_user_info(user_id):
    sql = "SELECT * FROM users WHERE id = ?"
    with db.DatabaseCursor() as cursor:
        user = cursor.execute(sql, (user_id,)).fetchone()
    return user


def get_all_users():
    sql = "SELECT u.id, u.name, u.email FROM users AS u"
    with db.DatabaseCursor() as cursor:
        rows = cursor.execute(sql).fetchall()
    return rows


def get_number_of_users():
    sql = "SELECT COUNT(*) as count FROM users"
    with db.DatabaseCursor() as cursor:
        row = cursor.execute(sql).fetchone()
    return row['count']


# Password stuff from:
# http://stackoverflow.com/questions/2572099/pythons-safest-method-to-store-and-retrieve-passwords-from-a-database
def get_hexdigest(str1, str2):
    return hashlib.sha1('%s%s' % (str1, str2)).hexdigest()


def get_password_hash(raw_pwd):
    m = hashlib.sha1()
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_pwd)
    return '%s$%s' % (salt, hsh)


def check_password(raw_pwd, pwd_hash):
    salt, hsh = pwd_hash.split('$')
    return hsh == get_hexdigest(salt, raw_pwd)

