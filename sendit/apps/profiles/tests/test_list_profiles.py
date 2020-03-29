from rest_framework.views import status

from sendit.apps.core.tests.base_test import TestBaseCase


class TestListUserProfiles(TestBaseCase):
    def test_authenticated_user_list_profiles(self):
        self.regular_signup()
        self.regular_signup2()
        response = self.client.get(
            self.list_users_url,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token(),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated_user_list_profiles(self):
        self.regular_signup()
        self.regular_signup2()
        response = self.client.get(self.list_users_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
