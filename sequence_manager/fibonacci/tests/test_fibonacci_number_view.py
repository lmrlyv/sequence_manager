import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class FibonacciNumberViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_fib_number_success(self):
        """Test getting fibonacci number for a valid input."""
        response = self.client.get(reverse("fibonacci-number", args=[8]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertDictEqual(response_data["data"], {"number": 8, "value": 13})

    def test_get_fib_number_validation_error(self):
        """Test getting fibonacci number for an invalid input."""
        response = self.client.get(reverse("fibonacci-number", args=[0]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(
            response_data["error"]["number"][0], "Ensure this value is greater than or equal to 1."
        )

    def test_get_blacklisted_fib_number(self):
        """Test getting fibonacci number that has been blacklisted."""
        response = self.client.post(reverse("manage-blacklist", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["success"])

        response = self.client.get(reverse("fibonacci-number", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "This number is blacklisted and cannot be used.")
