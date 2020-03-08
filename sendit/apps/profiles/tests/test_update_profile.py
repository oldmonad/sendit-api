from rest_framework.views import status

from sendit.apps.core.tests.base_test import TestBaseCase


class TestUpdateUserProfile(TestBaseCase):
    def base_update_test(self, token):
        return self.client.put(
            self.get_profile_url(self.email),
            data=self.user_profile,
            format="json",
            HTTP_AUTHORIZATION="Token " + token,
        )

    def base_get_profile(self):
        return self.client.get(self.get_profile_url(self.email), format="json")

    def test_get_user_profile(self):
        self.signup_user()
        response = self.base_get_profile()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_no_user_profile(self):
        response = self.base_get_profile()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_profile(self):
        response = self.base_update_test(self.token())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_update_user_profile(self):
        response = self.base_update_test(self.invalid_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
