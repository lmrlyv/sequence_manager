from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class FibonacciNumberListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_fib_list_success(self):
        """Test retrieving list of fibonacci numbers for a valid input."""
        response = self.client.get(reverse("fibonacci-list", args=[8]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertDictEqual(
            response_data["data"],
            {
                "count": 8,
                "next": None,
                "previous": None,
                "results": [
                    {"number": 1, "value": 0},
                    {"number": 2, "value": 1},
                    {"number": 3, "value": 1},
                    {"number": 4, "value": 2},
                    {"number": 5, "value": 3},
                    {"number": 6, "value": 5},
                    {"number": 7, "value": 8},
                    {"number": 8, "value": 13},
                ],
            },
        )

    def test_get_fib_list_success_with_blacklisted_number(self):
        """Test blacklisted number are excluded from the list of fibonacci numbers."""
        response = self.client.post(reverse("manage-blacklist", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["success"])

        response = self.client.post(reverse("manage-blacklist", args=[5]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()["success"])

        # Test if 3 and 5 are excluded in the response
        response = self.client.get(reverse("fibonacci-list", args=[8]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertDictEqual(
            response_data["data"],
            {
                "count": 6,
                "next": None,
                "previous": None,
                "results": [
                    {"number": 1, "value": 0},
                    {"number": 2, "value": 1},
                    {"number": 4, "value": 2},
                    {"number": 6, "value": 5},
                    {"number": 7, "value": 8},
                    {"number": 8, "value": 13},
                ],
            },
        )

    def test_get_fib_list_validation_error(self):
        """Test retrieving list of fibonacci numbers for an invalid input."""
        response = self.client.get(reverse("fibonacci-list", args=[0]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(
            response_data["error"]["number"][0], "Ensure this value is greater than or equal to 1."
        )

    def test_get_fib_list_with_default_page_size(self):
        """Test retrieving list of fibonacci numbers without page_size parameter."""
        response = self.client.get(reverse("fibonacci-list", args=[113]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"]["count"], 113)
        self.assertIsNotNone(response_data["data"]["next"])
        self.assertEqual(len(response_data["data"]["results"]), 100)

    def test_get_fib_list_with_custom_page_size(self):
        """Test retrieving list of fibonacci numbers with custom page_size parameter."""
        response = self.client.get(reverse("fibonacci-list", args=[10]), data={"page_size": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"]["count"], 10)
        self.assertIsNotNone(response_data["data"]["next"])
        self.assertEqual(len(response_data["data"]["results"]), 3)

    def test_get_fib_list_with_different_page_value(self):
        """Test retrieving list of fibonacci numbers with custom page_size parameter."""
        params = {"page_size": 3, "page": 2}
        response = self.client.get(reverse("fibonacci-list", args=[10]), data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"]["count"], 10)
        self.assertIsNotNone(response_data["data"]["next"])
        self.assertIsNotNone(response_data["data"]["previous"])
        self.assertEqual(len(response_data["data"]["results"]), 3)
        self.assertListEqual(
            response_data["data"]["results"],
            [
                {"number": 4, "value": 2},
                {"number": 5, "value": 3},
                {"number": 6, "value": 5},
            ],
        )

    def test_get_fib_list_with_invalid_page_value(self):
        """Test retrieving list of fibonacci numbers with custom page_size parameter."""
        params = {"page_size": 3, "page": 5}
        response = self.client.get(reverse("fibonacci-list", args=[10]), data=params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"], "Invalid page")
