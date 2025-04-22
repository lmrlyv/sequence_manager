from django.db import IntegrityError
from rest_framework.exceptions import APIException

from sequence_manager.fibonacci.models import BlacklistedFibonacciNumber
from sequence_manager.fibonacci.utils.api_exceptions import (
    BlacklistConflictApiException,
    BlacklistNotFoundApiException,
)


class FibonacciSequenceService:
    """Service class for calculating Fibonacci numbers."""

    def get_fib_number(self, index: int) -> int:
        """Returns the Fibonacci number at the given index.

        Args:
            index (int): The index in the Fibonacci sequence (0-based).

        Returns:
            int: The Fibonacci number at the specified index.

        Raises:
            ValueError: If the input index is negative.
        """
        if index < 0:
            raise ValueError("The 'index' argument cannot be negative.")

        if index <= 1:
            return index

        prev2, prev1 = 0, 1
        for _ in range(2, index + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1

    def get_all_fib_numbers(self, index: int) -> list[int]:
        """Returns a list of Fibonacci numbers up to the given index.

        Args:
            number (int): The upper bound index for which to generate Fibonacci numbers.

        Returns:
            list[int]: A list of Fibonacci numbers up to the specified index.

        Raises:
            ValueError: If the input number is negative.
        """
        if index < 0:
            raise ValueError("The 'index' argument cannot be negative.")

        if index == 0:
            return [0]

        fibs = [0, 1]
        for _ in range(2, index + 1):
            fibs.append(fibs[-1] + fibs[-2])
        return fibs


class BlacklistFibonacciNumberService:
    """Service for managing blacklisted Fibonacci numbers.

    Provides methods to add and remove Fibonacci numbers from a blacklist.
    Handles validation and raises appropriate API exceptions for duplicate
    or missing entries.
    """

    def add_to_blacklist(self, number: int):
        """Adds a Fibonacci number to the blacklist.

        Args:
            number (int): The Fibonacci number to blacklist.

        Raises:
            BlacklistConflictApiException: If the number is already blacklisted.
            APIException: For any unexpected errors during the operation.
        """
        try:
            BlacklistedFibonacciNumber.objects.create(number=number)
        except IntegrityError:
            # Handle the case where there is a constraint violation (e.g. uniqueness)
            raise BlacklistConflictApiException()
        except Exception as err:
            raise APIException(detail=f"Unexpected error: {err}")

    def remove_from_blacklist(self, number: int):
        """Removes a Fibonacci number from the blacklist.

        Args:
            number (int): The Fibonacci number to remove.

        Raises:
            BlacklistNotFoundApiException: If the number is not found in the blacklist.
            APIException: For any unexpected errors during the operation.
        """
        try:
            obj = BlacklistedFibonacciNumber.objects.get(number=number)
            obj.delete()
        except BlacklistedFibonacciNumber.DoesNotExist:
            raise BlacklistNotFoundApiException()
        except Exception as err:
            raise APIException(detail=f"Unexpected error: {err}")
