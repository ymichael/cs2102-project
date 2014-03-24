import db
import model
import hashlib
import random

class User(model.base.BaseModel):
    properties = [
        'name',
        'email',
        'bio',
        'create_time',
    ]

    def __init__(self, user_id=None):
        self.id = user_id

    def check_is_saved(self):
        return self.id

    def get(self):
        return get_user_info(self.id)

    def put(self):
        update_existing_user(self.id, self.name, self.email)

    def post(self):
        raise Exception("Use model.user.create_new_user instead.")

    def validate(self):
        # TODO(michael): Add validation
        return (self.name and self.email and self.id)


def update_existing_user(user_id, name, email):
    sql = """\
        UPDATE users
        SET name = ?, email = ?
        WHERE uid = ?"""
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


def verify_login(email, password):
    sql = "SELECT uid, password_hash FROM users WHERE email = ?"
    with db.DatabaseCursor() as cursor:
        user = cursor.execute(sql, (email,)).fetchone()

    if user is None:
        return False

    if check_password(password, user['password_hash']):
        return user['uid']

    return False


def get_user_info(user_id):
    sql = "SELECT * FROM users WHERE uid = ?"
    with db.DatabaseCursor() as cursor:
        user = cursor.execute(sql, (user_id,)).fetchone()
    return user

def get_all_users():
    sql = "SELECT u.uid, u.name, u.email FROM users AS u"
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

