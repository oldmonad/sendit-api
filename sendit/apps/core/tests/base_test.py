from django.urls import reverse
from rest_framework.test import APITestCase

from sendit.apps.authentication.models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse("app_authentication:signup")
        self.login_url = reverse("app_authentication:login")
        self.current_user_url = reverse("app_authentication:current_user")
        self.invalid_token = "thsnmbnscjkxcmm.btydghvhjb"
        self.list_users_url = reverse("profiles:profile_list")

        self.no_email = ["email"]
        self.no_full_name = ["full_name"]
        self.no_password = ["password"]

        self.user_email = None

        self.test_user = {
            "user": {
                "full_name": "testuser",
                "email": "test@user.com",
                "password": "TestUser123",
            }
        }

        self.test_user2 = {
            "user": {
                "full_name": "testuser2",
                "email": "test2@user.com",
                "password": "TestUser123",
            }
        }

        self.user_profile = {
            "profile": {
                "address": "Onipanu crecent",
                "image": "https://static.productionready.io/images/smiley-cyrus.jpg",
            }
        }

        self.email = self.test_user["user"]["email"]
        self.no_email = ["email"]
        self.no_full_name = ["full_name"]
        self.no_password = ["password"]
        self.passwords = {
            "password": "Password0007",
            "confirm_password": "Password0007",
        }

    def remove_data(self, keys=None):
        if keys:
            for key in keys:
                del self.test_user["user"][key]
        return self.test_user

    def signup_user(self):
        return self.client.post(self.signup_url, self.test_user, format="json")

    def signup_user2(self):
        return self.client.post(self.signup_url, self.test_user2, format="json")

    def activateable_user(self, user_email):
        try:
            self.user_email = User.objects.get(email=user_email)
            if self.user_email:
                self.user_email.is_verified = True
                self.user_email.is_active = True
                self.user_email.save()
                return True
        except User.DoesNotExist:
            return False

    def login_user(self):
        self.remove_data(self.no_full_name)
        if "email" in self.test_user["user"]:
            activateable_user = self.activateable_user(self.test_user["user"]["email"])
            if not activateable_user:
                return self.client.post(self.login_url, self.test_user, format="json")

        return self.client.post(self.login_url, self.test_user, format="json")

    def token(self):
        self.signup_user()
        return self.login_user().data["token"]

    def get_profile_url(self, email):
        return reverse("profiles:user_profile", args={email})
