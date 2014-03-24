from tests import assert_eq
import tests
import model


def test_password():
    password = 'password'
    hsh = model.user.get_password_hash(password)
    assert model.user.check_password(password, hsh)


@tests.prepare
def test_user_creation():
    assert_eq(model.user.get_number_of_users(), 0)

    user_id = model.user.create_new_user(
        'michael', 'michael@test.com', 'mypassword')

    assert_eq(model.user.get_number_of_users(), 1)

    user = model.user.User(user_id)
    assert_eq(user.id, user_id)
    assert_eq(user.name, 'michael')
    assert_eq(user.email, 'michael@test.com')


@tests.prepare
def test_user_update_and_save():
    assert_eq(model.user.get_number_of_users(), 0)

    user_id = model.user.create_new_user(
        'michael', 'michael@test.com', 'mypassword')

    assert_eq(model.user.get_number_of_users(), 1)

    user = model.user.User(user_id)
    assert_eq(user.id, user_id)
    assert_eq(user.name, 'michael')
    assert_eq(user.email, 'michael@test.com')

    user.name = 'John'
    user.bio = 'asdf'
    user.save()

    new_user_obj = model.user.User(user_id)
    assert_eq(new_user_obj.name, 'John')
    assert_eq(new_user_obj.bio, 'asdf')


@tests.prepare
def test_non_existent_user():
    assert_eq(model.user.get_number_of_users(), 0)
    user = model.user.User(10)
    assert not user.name
    assert not user.email

    user = model.user.User()
    assert not user.name
    assert not user.email
