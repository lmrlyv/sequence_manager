from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from sequence_manager.utils.custom_responses import JsonResponseError, JsonResponseSuccess


class FibonacciNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def paginate(self, queryset, request):
        try:
            paginated_data = self.paginate_queryset(queryset, request)
            response = self.get_paginated_response(paginated_data)
            return JsonResponseSuccess(response.data)
        except NotFound as err:
            return JsonResponseError("Invalid page", status=400)
