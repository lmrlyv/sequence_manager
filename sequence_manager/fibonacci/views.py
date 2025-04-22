import logging

from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class FibonacciValueView(APIView):

    def get(self, request: Request, number: int, *args, **kwargs):
        return JsonResponse({"number": 6, "value": 5})


class FibonacciListView(APIView):

    def get(self, request: Request, *args, **kwargs):
        return JsonResponse(
            {
                "data": [
                    {"number": 1, "value": 0},
                    {"number": 2, "value": 1},
                    {"number": 3, "value": 1},
                    {"number": 4, "value": 2},
                    {"number": 5, "value": 3},
                    {"number": 6, "value": 5},
                ]
            }
        )


class BlacklistNumberView(APIView):
    def post(self, request, number, *args, **kwargs):
        return JsonResponse({"data": f"Number {number} is blacklisted!"})

    def delete(self, request, number, *args, **kwargs):
        return JsonResponse({"data": f"Number {number} is deleted from the blacklist!"})
