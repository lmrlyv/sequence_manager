import logging

from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView

from sequence_manager.fibonacci.serializers import FibonacciNumberSerializer
from sequence_manager.fibonacci.services import BlacklistService, FibonacciSequenceService
from sequence_manager.fibonacci.utils.paginators import FibonacciNumberPagination
from sequence_manager.utils.custom_responses import JsonResponseError, JsonResponseSuccess


logger = logging.getLogger(__name__)


class FibonacciNumberView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
        """Retrieve the value from the Fibonacci sequence for a given number.

        GET /api/v1/fibonacci/<number>/

        Description:
            This endpoint returns the Fibonacci number at the specified position.

        Parameters:
            number (int): The 1-based index in the Fibonacci sequence. Must be a positive integer.

        Responses:
            200 OK:
                Description: Fibonacci number successfully retrieved.
                Example:
                {
                    "success": true,
                    "data": {
                        "number": 5,
                        "value": 3
                    }
                }
            400 Bad Request:
                Description: The input number is invalid (e.g., not greater than 1).
                Example:
                {
                    "success": false,
                    "error": {
                        "number": [
                            "Ensure this value is greater than or equal to 1."
                        ]
                    },
                    "message": "Validation error"
                }
            403 Forbidden:
                Description: The requested number is blacklisted and cannot be retrieved.
                Example:
                {
                    "success": false,
                    "error": "This number is blacklisted and cannot be used."
                }
        """
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponseError(serializer.errors, message="Validation error", status=400)

        if BlacklistService().is_blacklisted(number):
            return JsonResponseError("This number is blacklisted and cannot be used.", status=403)

        fib_num = FibonacciSequenceService().get_fib_number(number - 1)
        return JsonResponseSuccess({"number": number, "value": fib_num})


class FibonacciNumberListView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
        """Retrieve a list of Fibonacci numbers up to a given position, excluding blacklisted values.

        GET /api/v1/fibonacci/list/<number>/

        Description:
            This endpoint returns a list of Fibonacci numbers from position 1 up to the given number,
            omitting any numbers that are currently blacklisted. The results are paginated, and
            clients can customize the page size using the `page_size` query parameter.

        Parameters:
            number (int): The upper limit (inclusive) of the Fibonacci sequence to return.
                          Must be a positive integer.

            Query Parameters:
                page (int, optional): The page number to retrieve (default: 1).
                page_size (int, optional): Number of items per page (default: 100).

        Responses:
            200 OK:
                Description: A paginated list of Fibonacci numbers, excluding blacklisted ones.
                Example:
                {
                    "success": true,
                    "data": {
                        "count": 100,
                        "next": null,
                        "previous": null,
                        "results": [
                            {"number": 1, "value": 0},
                            {"number": 2, "value": 1},
                            {"number": 3, "value": 1},
                            ...
                        ]
                    }
                }

            400 Bad Request:
                Description: The input number is invalid (e.g., not greater than 1).
                Example:
                {
                    "success": false,
                    "error": {
                        "number": [
                            "Ensure this value is greater than or equal to 1."
                        ]
                    },
                    "message": "Validation error"
                }
        """
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponseError(serializer.errors, message="Validation error", status=400)

        fib_nums = FibonacciSequenceService().get_all_fib_numbers(number - 1)

        blacklisted_numbers = BlacklistService().get_blacklisted_numbers()

        response_data = [
            {"number": idx + 1, "value": num}
            for idx, num in enumerate(fib_nums)
            if (idx + 1) not in blacklisted_numbers
        ]

        paginator = FibonacciNumberPagination()
        return paginator.paginate(response_data, request)


class BlacklistNumberView(APIView):
    def post(self, request, number, *args, **kwargs):
        """Add a Fibonacci number to the blacklist.

        POST /api/v1/fibonacci/blacklist/<number>/

        Description:
            This endpoint adds the specified Fibonacci number to the blacklist. Once blacklisted,
            the number will be excluded from future Fibonacci sequence responses.

        Parameters:
            number (int): The Fibonacci number to blacklist. Must be a positive integer.

        Responses:
            201 Created:
                Description: The number was successfully added to the blacklist.
                Example:
                {
                    "success": true,
                    "data": "Number 13 has been added to the blacklist!"
                }

            400 Bad Request:
                Description: The input number is invalid (e.g., not greater than 1).
                Example:
                {
                    "success": false,
                    "error": {
                        "number": [
                            "Ensure this value is greater than or equal to 1."
                        ]
                    },
                    "message": "Validation error"
                }

            409 Conflict:
                Description: The number is already in the blacklist.
                Example:
                {
                    "success": false,
                    "error": "This Fibonacci number is already blacklisted."
                }
        """
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponseError(serializer.errors, message="Validation error", status=400)

        BlacklistService().add_to_blacklist(number)

        return JsonResponseSuccess(f"Number {number} has been added to the blacklist!", status=201)

    def delete(self, request, number, *args, **kwargs):
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponseError(serializer.errors, message="Validation error", status=400)

        BlacklistService().remove_from_blacklist(number)

        return JsonResponseSuccess(f"Number {number} has been deleted from the blacklist!")
