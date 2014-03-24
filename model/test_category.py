import tests
import model
import db

from tests import assert_eq

@tests.prepare
def test_create_category():
    cat = model.category.Category()
    cat.label = 'HOUSE'
    cat_id = cat.save()

    new_cat = model.category.Category(cat_id)
    assert_eq('HOUSE', new_cat.label)


@tests.prepare
def test_add_listing_to_category():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)

    cat = model.category.Category()
    cat.label = 'HOUSE'
    cat_id = cat.save()

    assert_eq(0, len(model.category.listing_categories(lid)))
    model.category.add_listing_to_category(
        lid, cat_id)
    assert_eq(1, len(model.category.listing_categories(lid)))


@tests.prepare
def test_remove_listing_from_category():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)

    cat = model.category.Category()
    cat.label = 'HOUSE'
    cat_id = cat.save()

    assert_eq(0, len(model.category.listing_categories(lid)))
    model.category.add_listing_to_category(
        lid, cat_id)
    assert_eq(1, len(model.category.listing_categories(lid)))
    model.category.remove_listing_from_category(
        lid, cat_id)
    assert_eq(0, len(model.category.listing_categories(lid)))


@tests.prepare
def test_cat_ids_to_labels():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)

    cat_ids = []
    for label in ['HOUSE', "ASDF"]:
        cat = model.category.Category()
        cat.label = label
        cat_id = cat.save()
        cat_ids.append(cat_id)

    assert_eq(
        ['HOUSE', 'ASDF'],
        model.category.cat_ids_to_labels(cat_ids))


@tests.prepare
def test_create_or_retrieve_category():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)

    cat = model.category.Category()
    cat.label = 'HOUSE'
    cat_id = cat.save()

    assert_eq(cat_id,
        model.category.create_or_retrieve_category('HOUSE'))

    cat_id2 = model.category.create_or_retrieve_category('APPLE')
    assert_eq('APPLE', model.category.Category(cat_id2).label)