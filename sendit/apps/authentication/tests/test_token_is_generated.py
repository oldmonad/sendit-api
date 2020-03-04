# Django imports
from rest_framework.views import status

from ..models import User

# local imports
from .base_test import TestBaseCase


class JwtTestCase(TestBaseCase):
    def base_token(self, message):
        response = self.client.get(self.current_user_url)
        assert response.status_code == 403
        assert response.data["detail"] == message

    def test_token_on_register(self):
        """if user is registers successfully, a token is generated"""

        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["user_info"])

    def test_token_on_login(self):
        """Test if a user logs in successfully, a token is generated"""
        self.signup_user()
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_get_current_user(self):
        """Test to get current user when token is passed in the request"""
        self.signup_user()
        token = self.login_user().data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(self.current_user_url)
        assert response.status_code == 200
        assert response.data["email"] == "test@user.com"
        assert response.data["username"] == "testuser"

    def test_get_user_no_token(self):
        """Test getting a user with no token provided in the request"""

        self.base_token("Authentication credentials were not provided.")

    def test_get_user_invalid_token(self):
        """Test getting a user with an expired or invalid token"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.invalid_token)
        self.base_token("Invalid token")

    def test_get_non_existent_user(self):
        """Test getting a user who doesn't exist in db"""
        self.signup_user()
        token = self.login_user().data["token"]
        User.objects.get(email=self.test_user["user"]["email"]).delete()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.base_token("User does not exist")
