from django.test import TestCase

from ..models import User


class UserModelTestCase(TestCase):
    """
    This the test suite for the User mode class
    """

    def test_create_user(self):
        """
        This is to test that the user model can
        successfully create a user.
        """
        self.assertIsInstance(
            User.objects.create_user(
                username="username", password="password", email="user@mail.com"
            ),
            User,
        )
