from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status

from sendit.apps.authentication.models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse("app_authentication:signup")
        self.login_url = reverse("app_authentication:login")
        self.current_user_url = reverse("app_authentication:current_user")
        self.invalid_token = "thsnmbnscjkxcmm.btydghvhjb"
        self.list_users_url = reverse("profiles:profile_list")
        self.create_list_parcel_url = reverse("parcels:parcels")

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

        self.test_admin_user = {
            "user": {
                "full_name": "testadminuser",
                "email": "admin_test@user.com",
                "password": "TestUser123",
            }
        }

        self.user_profile = {
            "profile": {
                "address": "Onipanu crecent",
                "image": "https://static.productionready.io/images/smiley-cyrus.jpg",
            }
        }

        self.parcel = {
            "parcel": {
                "pickup_location": "Pickup location",
                "destination": "Destination yup",
                "present_location": "Present location",
                "weight": "50",
                "quote": "503",
            }
        }

        self.update_parcel_data = {
            "parcel": {
                "pickup_location": "Updated Pickup location",
                "destination": "Updated Destination yup",
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

    def signup_user(self, user_input, user_type):
        response = self.client.post(self.signup_url, user_input, format="json")
        if response.status_code == 201:
            self.user_email = User.objects.get(email=user_input["user"]["email"])
            if self.user_email:
                self.user_email.is_verified = True
                self.user_email.is_active = True
                if user_type == "admin":
                    self.user_email.is_staff = True
                self.user_email.save()
        return response

    def regular_signup(self):
        return self.signup_user(self.test_user, "regular_signup")

    def regular_signup2(self):
        return self.signup_user(self.test_user2, "regular_signup")

    def admin_signup(self):
        return self.signup_user(self.test_admin_user, "admin")

    def login_user(self, user_input, remove_field):
        for field in remove_field:
            if field in user_input:
                self.remove_data(remove_field)
        return self.client.post(self.login_url, user_input, format="json")

    def regular_login(self):
        return self.login_user(self.test_user, self.no_full_name)

    def regular_login2(self):
        return self.login_user(self.test_user2, self.no_full_name)

    def admin_login(self):
        return self.login_user(self.test_admin_user, self.no_full_name)

    def regular_token(self):
        self.regular_signup()
        return self.regular_login().data["token"]

    def regular_token2(self):
        self.regular_signup2()
        return self.regular_login2().data["token"]

    def admin_token(self):
        self.admin_signup()
        return self.admin_login().data["token"]

    def get_profile_url(self, email):
        return reverse("profiles:user_profile", args={email})

    def single_parcel_url(self, id):
        return reverse("parcels:parcel_details", args={id})
