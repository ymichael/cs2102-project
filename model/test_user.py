import tests
import model
import config


def test_password():
    password = 'password'
    hsh = model.user.get_password_hash(password)
    assert model.user.check_password(password, hsh)


@tests.manage
def test_user_creation():
    assert model.user.get_number_of_users() == 0

    model.user.create_new_user(
        'Michael',
        'michael@test.com',
        'mypassword')

    assert model.user.get_number_of_users() == 1
