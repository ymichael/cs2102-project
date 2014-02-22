import db
import hashlib
import random

def create_new_user(name, email, password):
    password_hash = get_password_hash(password)
    sql = """\
        INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)"""

    database = db.connect_db()
    cursor = database.cursor()
    cursor.execute(sql, (name, email, password_hash))
    database.commit()
    database.close()


def get_all_users():
    sql = "SELECT u.id, u.name, u.email FROM users AS u"
    database = db.connect_db()
    cursor = database.cursor()
    rows = cursor.execute(sql).fetchall()
    database.close()

    users = []
    for user in rows:
        users.append({
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        })
    return users


def get_number_of_users():
    sql = "SELECT COUNT(*) as count FROM users"
    database = db.connect_db()
    cursor = database.cursor()
    row = cursor.execute(sql).fetchone()
    database.close()
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

