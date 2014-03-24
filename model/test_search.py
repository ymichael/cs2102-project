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

    assert_eq(3, len(model.search.listing_search('apple')))
    assert_eq(3, len(model.search.listing_search('orange')))
    assert_eq(4, len(model.search.listing_search('pear')))
    assert_eq(4, len(model.search.listing_search('peach')))
    assert_eq(0, len(model.search.listing_search('grapes')))


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

    assert_eq(3, len(model.search.listing_search('pineapple')))
    assert_eq(2, len(model.search.listing_search('mango')))
    assert_eq(2, len(model.search.listing_search('pear')))


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