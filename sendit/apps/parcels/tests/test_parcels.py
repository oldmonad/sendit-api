from rest_framework.views import status

from sendit.apps.core.tests.base_test import TestBaseCase


class TestCreateParcelOrder(TestBaseCase):
    def base_parcels(self, message, response):
        self.assertIn(message.encode(), response.content)

    def regular_authorized_post_request(self, url):
        return self.client.post(
            url,
            self.parcel,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token(),
        )

    def regular_get_request(self, url):
        return self.client.get(
            url, format="json", HTTP_AUTHORIZATION="Token " + self.regular_token()
        )

    def admin_get_request(self, url):
        return self.client.get(
            url, format="json", HTTP_AUTHORIZATION="Token " + self.admin_token()
        )

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_parcel_order(self):
        """
        This method checks if a user can create a parcel order
        """

        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.base_parcels("Pickup location", response)
        self.base_parcels("Destination yup", response)
        self.base_parcels("Present location", response)
        self.base_parcels("50", response)
        self.base_parcels("503", response)

    def test_user_can_create_parcel_order_without_present_location(self):
        """
        This method checks if a user can create a parcel order without present location
        """

        self.parcel["parcel"].pop("present_location")
        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.base_parcels("Pickup location", response)
        self.base_parcels("Destination yup", response)
        self.base_parcels("50", response)
        self.base_parcels("503", response)

    def test_create_parcels_unauthorized(self):
        """
        This method tests that unathorized user cannot create parcel deliveries
        """
        response = self.client.post(
            self.create_list_parcel_url, self.parcel, format="json"
        )
        self.http_403_forbidden(response)
        self.base_parcels("Authentication credentials were not provided.", response)

    def test_user_cannot_create_without_pickup_location(self):
        """
        This method makes sure a parcel delivery cannot be created without pick up location input
        """
        self.parcel["parcel"].pop("pickup_location")
        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.base_parcels("Pickup location is required", response)

    def test_user_cannot_create_without_destination(self):
        """
         This method makes sure a parcel delivery cannot be created without destination input
        """
        self.parcel["parcel"].pop("destination")
        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.base_parcels("Destination is required", response)

    def test_user_cannot_create_without_weight(self):
        """
        This method makes sure a parcel delivery cannot be created without weight input
        """
        self.parcel["parcel"].pop("weight")
        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.base_parcels("Weight is required", response)

    def test_user_cannot_create_without_quote(self):
        """
        This method makes sure a parcel delivery cannot be created without quote input
        """
        self.parcel["parcel"].pop("quote")
        response = self.regular_authorized_post_request(self.create_list_parcel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.base_parcels("Quote is required", response)

    def test_admin_get_parcels(self):
        """
        This method tests that only an admin can successfully retrieve all parcel deliveries
        """
        response = self.admin_get_request(self.create_list_parcel_url)
        self.http_200_ok(response)

    def test_get_parcels_unauthorized(self):
        """
        This method tests that unathorized user cannot retrieve parcel deliveries
        """
        response = self.client.get(
            self.create_list_parcel_url, self.parcel, format="json"
        )
        self.http_403_forbidden(response)
        self.base_parcels("Authentication credentials were not provided.", response)

    def test_get_parcels_non_admin_user(self):
        """
        This method tests that a non-admin user cannot retrieve parcel deliveries
        """
        response = self.regular_get_request(self.create_list_parcel_url)
        self.http_403_forbidden(response)
        self.base_parcels(
            "You do not have permission to perform this action.", response
        )

    def test_user_can_update(self):
        """
        This method checks if a user can update an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.put(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token(),
        )
        self.base_parcels("Updated Pickup location", response)
        self.http_200_ok(response)
        self.base_parcels("Pickup location", created_article)

    def test_admin_can_update(self):
        """
        This method checks if a admin can update an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.put(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.admin_token(),
        )
        self.base_parcels("Updated Pickup location", response)
        self.http_200_ok(response)
        self.base_parcels("Pickup location", created_article)

    def test_non_creator_cant_update(self):
        """
        This method checks that a non-creator of a resource can't update it
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.put(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token2(),
        )
        self.http_403_forbidden(response)
        self.base_parcels(
            "You do not have permission to perform this action.", response
        )

    def test_user_can_retrieve(self):
        """
        This method checks if a user can retrieve an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.get(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token(),
        )
        self.http_200_ok(response)
        self.base_parcels("Pickup location", response)
        self.base_parcels("Destination yup", response)
        self.base_parcels("50", response)
        self.base_parcels("503", response)

    def test_admin_can_retrieve(self):
        """
        This method checks if an admin can retrieve an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.get(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.admin_token(),
        )
        self.http_200_ok(response)
        self.base_parcels("Pickup location", response)
        self.base_parcels("Destination yup", response)
        self.base_parcels("50", response)
        self.base_parcels("503", response)

    def test_non_creator_cant_retrieve(self):
        """
        This method checks that a non-creator of a resource can't retrieve it
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.get(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token2(),
        )
        self.http_403_forbidden(response)
        self.base_parcels(
            "You do not have permission to perform this action.", response
        )

    def test_user_can_delete(self):
        """
        This method checks if a user can delete an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.delete(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token(),
        )
        self.http_200_ok(response)
        self.base_parcels("Parcel Deleted Successfully", response)

    def test_amin_can_delete(self):
        """
        This method checks if an admin can delete an existing parcel delivery
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.delete(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.admin_token(),
        )
        self.http_200_ok(response)
        self.base_parcels("Parcel Deleted Successfully", response)

    def test_non_creator_cant_delete(self):
        """
        This method checks that a non-creator of a resource can't delete it
        """

        created_article = self.regular_authorized_post_request(
            self.create_list_parcel_url
        )
        url = self.single_parcel_url(created_article.data["id"])
        response = self.client.delete(
            url,
            self.update_parcel_data,
            format="json",
            HTTP_AUTHORIZATION="Token " + self.regular_token2(),
        )
        self.http_403_forbidden(response)
        self.base_parcels(
            "You do not have permission to perform this action.", response
        )
