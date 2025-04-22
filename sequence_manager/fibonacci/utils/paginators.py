from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class FibonacciNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def paginate(self, queryset, request):
        try:
            paginated_data = self.paginate_queryset(queryset, request)
            return self.get_paginated_response(paginated_data)
        except NotFound as err:
            return JsonResponse({"error": "Invalid page"}, status=400)
