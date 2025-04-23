from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class BlacklistNumberViewPostMethodTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_blacklist_fib_number_success(self):
        """Test adding fibonacci number into the blacklist for a valid input."""
        response = self.client.post(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"], "Number 13 has been added to the blacklist!")

    def test_blacklist_already_existing_fib_number(self):
        """Test adding the same fibonacci number into the blacklist twice."""
        response = self.client.post(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["success"])

        response = self.client.post(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "This Fibonacci number is already blacklisted.")

    def test_blacklist_fib_number_validation_error(self):
        """Test adding fibonacci number into the blacklist for an invalid input."""
        response = self.client.post(reverse("manage-blacklist", args=[0]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(
            response_data["error"]["number"][0], "Ensure this value is greater than or equal to 1."
        )


class BlacklistNumberViewDeleteMethodTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_removing_blacklisted_fib_number_success(self):
        """Test removing blacklisted fibonacci number for a valid input."""
        # Add 13 to the blacklist
        response = self.client.post(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["success"])

        # Remove 13 to test
        response = self.client.delete(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"], "Number 13 has been deleted from the blacklist!")

    def test_removing_nonexisting_fib_number(self):
        """Test removing fibonacci number that is not blacklisted."""
        response = self.client.delete(reverse("manage-blacklist", args=[13]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "This number is not found in the blacklist.")

    def test_removing_blacklisted_fib_number_validation_error(self):
        """Test removing blacklisted fibonacci number for an invalid input."""
        response = self.client.delete(reverse("manage-blacklist", args=[0]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(
            response_data["error"]["number"][0], "Ensure this value is greater than or equal to 1."
        )
