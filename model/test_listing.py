from tests import assert_eq
import tests
import model
import db


@tests.prepare
def test_create_listing():
    user_id = db.mock_data.create_fake_user()
    assert_eq(model.user.get_number_of_users(), 1)

    listing = model.listing.Listing()
    listing.title = 'My awesome thing.'
    listing.description = 'Blah blah'
    listing.owner_id = user_id
    listing_id = listing.save()

    new_listing_obj = model.listing.Listing(listing_id)
    assert_eq(new_listing_obj.title, 'My awesome thing.')
    assert_eq(new_listing_obj.description, 'Blah blah')
    assert_eq(new_listing_obj.owner_id, user_id)


@tests.prepare
def test_save_listing():
    user_id = db.mock_data.create_fake_user()
    assert_eq(model.user.get_number_of_users(), 1)

    listing = model.listing.Listing()
    listing.title = 'My awesome thing.'
    listing.description = 'Blah blah'
    listing.owner_id = user_id
    listing_id = listing.save()
    assert_eq(listing.id, listing_id)

    listing.title = 'Another title.'
    listing.save()
    assert_eq(listing.title, 'Another title.')
    assert listing.last_update_time != listing.create_time


@tests.prepare
def test_update_listing():
    user_id = db.mock_data.create_fake_user()
    assert_eq(model.user.get_number_of_users(), 1)

    listing = model.listing.Listing()
    listing.title = 'My awesome thing.'
    listing.description = 'Blah blah'
    listing.owner_id = user_id
    listing_id = listing.save()
    assert_eq(listing.id, listing_id)

    listing.title = 'Another title.'
    listing.save()

    assert_eq(listing.title, 'Another title.')
    assert_eq(listing.title, 'Another title.')


@tests.prepare
def test_cant_change_owner():
    user_id = db.mock_data.create_fake_user()
    assert_eq(model.user.get_number_of_users(), 1)

    listing = model.listing.Listing()
    listing.title = 'My awesome thing.'
    listing.description = 'Blah blah'
    listing.owner_id = user_id
    listing_id = listing.save()
    assert_eq(listing.id, listing_id)

    listing.owner_id = 2
    listing.save()
    # Unchanged.
    assert_eq(listing.owner_id, user_id)


@tests.prepare
def test_number_of_listings():
    user_id = db.mock_data.create_fake_user()
    assert_eq(model.listing.get_number_of_listings(), 0)

    model.listing.create_new_listing(
        'title', 'description', user_id)
    assert_eq(model.listing.get_number_of_listings(), 1)

    for _ in xrange(5):
        model.listing.create_new_listing(
            'title', 'description', user_id)
    assert_eq(model.listing.get_number_of_listings(), 6)


@tests.prepare
def test_all_listings():
    user_id = db.mock_data.create_fake_user()
    assert_eq(len(model.listing.get_all_listings()), 0)

    model.listing.create_new_listing(
        'title', 'description', user_id)
    assert_eq(len(model.listing.get_all_listings()), 1)


@tests.prepare
def test_get_latest_listings():
    user_id = db.mock_data.create_fake_user()
    assert_eq(len(model.listing.get_latest_listings(20)), 0)

    model.listing.create_new_listing(
        'title1', 'description', user_id)
    assert_eq(len(model.listing.get_latest_listings(20)), 1)

    model.listing.create_new_listing(
        'title2', 'description', user_id)

    model.listing.create_new_listing(
        'title3', 'description', user_id)
    assert_eq(len(model.listing.get_latest_listings(20)), 3)

    last_two_listings = model.listing.get_latest_listings(2)
    assert_eq(len(last_two_listings), 2)
    assert_eq(last_two_listings[0]['title'], 'title3')
    assert_eq(last_two_listings[1]['title'], 'title2')
