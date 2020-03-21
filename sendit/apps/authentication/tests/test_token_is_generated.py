# Django imports
from rest_framework.views import status

# local imports
from sendit.apps.core.tests.base_test import TestBaseCase

from ..models import User


class JwtTestCase(TestBaseCase):
    def base_token(self, message):
        response = self.client.get(self.current_user_url)
        assert response.status_code == 403
        assert response.data["detail"] == message

    def test_token_on_register(self):
        """if user is registers successfully, a token is generated"""

        response = self.regular_signup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["user_info"])

    def test_token_on_login(self):
        """Test if a user logs in successfully, a token is generated"""
        self.regular_signup()
        response = self.regular_login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_get_current_user(self):
        """Test to get current user when token is passed in the request"""
        self.regular_signup()
        token = self.regular_login().data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(self.current_user_url)
        assert response.status_code == 200
        assert response.data["email"] == "test@user.com"
        assert response.data["full_name"] == "testuser"

    def test_get_user_no_token(self):
        """Test getting a user with no token provided in the request"""

        self.base_token("Authentication credentials were not provided.")

    def test_get_user_invalid_token(self):
        """Test getting a user with an expired or invalid token"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.invalid_token)
        self.base_token("Invalid token")

    def test_get_non_existent_user(self):
        """Test getting a user who doesn't exist in db"""
        self.regular_signup()
        token = self.regular_login().data["token"]
        User.objects.get(email=self.test_user["user"]["email"]).delete()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.base_token("User does not exist")
