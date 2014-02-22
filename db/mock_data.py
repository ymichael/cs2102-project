# Use faker to bootstrap db with fake data.
import model
from faker import Factory

def maybe_add_mock_users(num):
    if model.user.get_number_of_users() == 0:
        fake = Factory.create()
        for _ in xrange(num):
            name = fake.name()
            email = fake.free_email()
            password = fake.sha1()[:10]
            model.user.create_new_user(name, email, password)


def maybe_bootstrap_db():
    maybe_add_mock_users(100)
