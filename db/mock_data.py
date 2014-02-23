# Use faker to bootstrap db with fake data.
import model
import random
from faker import Factory

def create_fake_user():
    fake = Factory.create()
    name = fake.name()
    email = fake.free_email()
    password = fake.sha1()[:10]
    return model.user.create_new_user(name, email, password)


def create_fake_owner_and_listings(num_of_listings=1):
    fake_owner = create_fake_user()
    fake = Factory.create()

    for _ in xrange(num):
        create_fake_listings(fake_owner)


def create_fake_listings(owner_id):
    fake = Factory.create()
    title = fake.bs()
    description = fake.paragraph()
    return model.listing.create_new_listing(title, description, owner_id)


def maybe_bootstrap_db():
    number_of_users = 200
    if model.user.get_number_of_users() == 0:
        for _ in xrange(number_of_users):
            user_id = create_fake_user()
        print 'INSERTED %s users.' % number_of_users

    min_listings = 0
    max_listings = 10
    if model.listing.get_number_of_listings() == 0:
        count = 0
        for user in model.user.get_all_users():
            for _ in xrange(random.randint(min_listings, max_listings)):
                count += 1
                create_fake_listings(user['id'])

        print 'INSERTED %s listings.' % count
