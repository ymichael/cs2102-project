from tests import assert_eq
import tests
import model
import db


@tests.prepare
def test_create_comment():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my comment'
    cid = comment.save()

    new_comment_obj = model.comment.Comment(cid)
    assert_eq('This is my comment', new_comment_obj.body)
    assert_eq(uid, new_comment_obj.uid)
    assert_eq(lid, new_comment_obj.lid)


@tests.prepare
def test_get_comments_for_listing():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)
    assert_eq(0, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my comment'
    cid1 = comment.save()
    assert_eq(1, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my second comment'
    cid2 = comment.save()
    assert_eq(2, len(model.comment.get_comments_for_listing(lid)))

    lid2 = db.mock_data.create_fake_listings(uid)
    comment = model.comment.Comment()
    comment.lid = lid2
    comment.uid = uid
    comment.body = 'This is my other comment'
    cid3 = comment.save()
    assert_eq(2, len(model.comment.get_comments_for_listing(lid)))
    assert_eq(1, len(model.comment.get_comments_for_listing(lid2)))


@tests.prepare
def test_get_comments_for_listing_time_order():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)
    assert_eq(0, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my comment'
    cid1 = comment.save()
    assert_eq(1, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my second comment'
    cid2 = comment.save()
    assert_eq(2, len(model.comment.get_comments_for_listing(lid)))

    comments = model.comment.get_comments_for_listing(lid)
    assert_eq(cid1, comments[0]['cid'])
    assert_eq(cid2, comments[1]['cid'])


@tests.prepare
def test_get_comments_for_listing_reverse_time_order():
    uid = db.mock_data.create_fake_user()
    lid = db.mock_data.create_fake_listings(uid)
    assert_eq(0, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my comment'
    cid1 = comment.save()
    assert_eq(1, len(model.comment.get_comments_for_listing(lid)))

    comment = model.comment.Comment()
    comment.lid = lid
    comment.uid = uid
    comment.body = 'This is my second comment'
    cid2 = comment.save()
    assert_eq(2, len(model.comment.get_comments_for_listing(lid)))

    comments = model.comment.get_comments_for_listing(lid, False)
    assert_eq(cid2, comments[0]['cid'])
    assert_eq(cid1, comments[1]['cid'])
