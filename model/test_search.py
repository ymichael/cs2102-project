from tests import assert_eq
import tests
import model
import db


listings = [
    ('mango', 'apple'),
    ('pear', 'orange'),
    ('peach', 'apple orange'),
    ('peach', 'pear'),
    ('peach', 'pear orange'),
    ('peach', 'apple pear'),
]

@tests.prepare
def test_listing_search_triggers():
    user_id = db.mock_data.create_fake_user()
    for title, description in listings:
        model.listing.create_new_listing(
            title, description, user_id)

    assert_eq(6, len(model.search.all_listing_search_entries()))


@tests.prepare
def test_listing_search_query():
    user_id = db.mock_data.create_fake_user()
    for title, description in listings:
        model.listing.create_new_listing(
            title, description, user_id)

    assert_eq(3, len(model.search.listings('apple', 20)))
    assert_eq(3, model.search.listings_count('apple'))
    assert_eq(3, len(model.search.listings('orange', 20)))
    assert_eq(3, model.search.listings_count('orange'))
    assert_eq(4, len(model.search.listings('pear', 20)))
    assert_eq(4, model.search.listings_count('pear'))
    assert_eq(4, len(model.search.listings('peach', 20)))
    assert_eq(4, model.search.listings_count('peach'))
    assert_eq(0, len(model.search.listings('grapes', 20)))
    assert_eq(0, model.search.listings_count('grapes'))


@tests.prepare
def test_listing_search_query_trigger_update():
    user_id = db.mock_data.create_fake_user()
    listing_ids = []
    for title, description in listings:
        ids = model.listing.create_new_listing(
            title, description, user_id)
        listing_ids.append(ids)

    for listing_id in listing_ids:
        l = model.listing.Listing(listing_id)
        if l.title == "pear":
            l.title = "mango"
        if "apple" in l.description:
            l.description = "pineapple"
        l.save()

    assert_eq(3, len(model.search.listings('pineapple', 20)))
    assert_eq(2, len(model.search.listings('mango', 20)))
    assert_eq(2, len(model.search.listings('pear', 20)))


@tests.prepare
def test_listing_search_query_trigger_delete():
    user_id = db.mock_data.create_fake_user()
    listing_ids = []
    for title, description in listings:
        ids = model.listing.create_new_listing(
            title, description, user_id)
        listing_ids.append(ids)

    for listing_id in listing_ids:
        l = model.listing.Listing(listing_id)
        l.delete()

    assert_eq(0, len(model.search.all_listing_search_entries()))