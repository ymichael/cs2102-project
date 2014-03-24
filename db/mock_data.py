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


def create_fake_comment(lid, uid):
    fake = Factory.create()
    body = fake.sentence()
    return model.comment.create_new_comment(body, uid, lid)


def maybe_bootstrap_db():
    # Users.
    number_of_users = 200
    if model.user.get_number_of_users() == 0:
        for _ in xrange(number_of_users):
            user_id = create_fake_user()
        print 'INSERTED %s users.' % number_of_users


    # Listings
    min_listings = 0
    max_listings = 10
    if model.listing.get_number_of_listings() == 0:
        count = 0
        for user in model.user.get_all_users():
            for _ in xrange(random.randint(min_listings, max_listings)):
                count += 1
                create_fake_listings(user['uid'])

        print 'INSERTED %s listings.' % count


    # Comments
    min_comments = 0
    max_comments = 5
    comment_count = 0
    comment_threshold = 10
    if model.comment.get_number_of_comments() < comment_threshold:
        for listing in model.listing.get_all_listings():
            # 20% of listings have no comments.
            if random.random() > 0.2:
                count = 0
                total_comments = random.randint(min_comments, max_comments)
                for user in model.user.get_all_users():
                    if count > total_comments:
                        break

                    if random.random() > 0.2:
                        create_fake_comment(listing['lid'], user['uid'])
                        count += 1
                        comment_count += 1
        print 'INSERTED %s comments.' % comment_count

    # Categories
    min_categories = 1
    max_categories = 3
    cat_count = 0
    catids = model.category.get_all_cat_ids()
    if model.category.number_of_listing_categories() == 0:
        for listing in model.listing.get_all_listings():
            for cat_id in random.sample(catids, random.randint(min_categories, max_categories)):
                model.category.add_listing_to_category(listing['lid'], cat_id)
                cat_count += 1
            
        print 'INSERTED %s listing_categories.' % cat_count