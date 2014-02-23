from tests import assert_eq
import tests
import model
import config


def test_password():
    password = 'password'
    hsh = model.user.get_password_hash(password)
    assert model.user.check_password(password, hsh)


@tests.prepare
def test_user_creation():
    assert_eq(model.user.get_number_of_users(), 0)

    user_name = 'Michael'
    user_email = 'michael@test.com'
    user_id = model.user.create_new_user(
        user_name, user_email, 'mypassword')

    assert_eq(model.user.get_number_of_users(), 1)

    user = model.user.User(user_id)
    assert_eq(user.user_id, user_id)
    assert_eq(user.name, user_name)
    assert_eq(user.email, user_email)


@tests.prepare
def test_non_existent_user():
    assert_eq(model.user.get_number_of_users(), 0)
    user = model.user.User(10)
    assert not user.name
    assert not user.email

    user = model.user.User()
    assert not user.name
    assert not user.email
