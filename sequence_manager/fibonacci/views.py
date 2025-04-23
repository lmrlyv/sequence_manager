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
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponseError(serializer.errors, message="Validation error", status=400)

        if BlacklistService().is_blacklisted(number):
            return JsonResponseError("This number is blacklisted and cannot be used.", status=403)

        fib_num = FibonacciSequenceService().get_fib_number(number - 1)
        return JsonResponseSuccess({"number": number, "value": fib_num})


class FibonacciNumberListView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
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
