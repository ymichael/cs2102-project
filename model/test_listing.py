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
    assert_eq(listing.listing_id, listing_id)

    listing.title = 'Another title.'
    listing.save()
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
    assert_eq(listing.listing_id, listing_id)

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


