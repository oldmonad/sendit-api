from rest_framework.views import status

# local imports
from sendit.apps.core.tests.base_test import TestBaseCase


class TestRegistration(TestBaseCase):
    """
    Handle tests for user registration
    """

    def base_signup(self, message, credentials=None):
        self.remove_data(credentials)
        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(message.encode(), response.content)

    def test_valid_user_registration(self):
        """
        User can be registered using the API
        """
        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_full_name_registration(self):
        """
        full_name is required for registration
        """
        message = "Full name is a required property"
        self.base_signup(message, self.no_full_name)

    def test_no_email_registration(self):
        """
        Email is required during registration
        """
        message = "Email is a required field"
        self.base_signup(message, self.no_email)

    def test_email_must_be_valid(self):
        """
        An email address must be of a valid format in order toregister
        """
        self.test_user["user"]["email"] = "Invalid-email"
        message = "Email must be of the format name@domain.com"
        self.base_signup(message)

    def test_no_password_registration(self):
        """
        Password is required during registration
        """
        message = "Password is a required field"
        self.base_signup(message, self.no_password)

    def test_short_password(self):
        """
        Password must be at least 8 characters
        """
        self.test_user["user"]["password"] = "pass07"
        message = "Password must be at least 8 characters long"
        self.base_signup(message)

    def test_alphanumeric_password(self):
        """
        Password must contain alphanumeric characters
        """
        self.test_user["user"]["password"] = "080696768"
        message = "Password must have at least a number, and a least an uppercase and a lowercase letter"
        self.base_signup(message)

    def test_full_name_is_required(self):
        """
        full_name is a required property
        """
        message = "Full name is a required property"
        self.base_signup(message, self.no_full_name)
