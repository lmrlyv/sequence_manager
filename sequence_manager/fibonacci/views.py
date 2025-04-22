import logging

from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView

from sequence_manager.fibonacci.serializers import FibonacciNumberSerializer
from sequence_manager.fibonacci.services import FibonacciSequenceService


logger = logging.getLogger(__name__)


class FibonacciNumberView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponse({"error": serializer.errors}, status=400)

        fib_num = FibonacciSequenceService().get_fib_number(number - 1)
        return JsonResponse({"number": number, "value": fib_num})


class FibonacciNumberListView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
        serializer = FibonacciNumberSerializer(data={"number": number})

        if not serializer.is_valid():
            return JsonResponse({"error": serializer.errors}, status=400)

        fib_nums = FibonacciSequenceService().get_all_fib_numbers(number - 1)
        response_data = [{"number": idx + 1, "value": num} for idx, num in enumerate(fib_nums)]

        return JsonResponse(response_data, safe=False)


class BlacklistNumberView(APIView):
    def post(self, request, number, *args, **kwargs):
        return JsonResponse({"data": f"Number {number} is blacklisted!"})

    def delete(self, request, number, *args, **kwargs):
        return JsonResponse({"data": f"Number {number} is deleted from the blacklist!"})
