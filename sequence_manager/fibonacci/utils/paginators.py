from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from sequence_manager.utils.custom_responses import JsonResponseError, JsonResponseSuccess


class FibonacciNumberPagination(PageNumberPagination):
    """Custom pagination class to enable client-controllable 'page_size' parameter.

    This pagination class allows clients to define the number of results per page
    by including a 'page_size' query parameter in their requests.
    """

    page_size_query_param = "page_size"

    def paginate(self, queryset, request):
        """Applies pagination to the given queryset and returns a paginated response.

        Args:
            queryset (QuerySet): The queryset to paginate.
            request (Request): The incoming request containing pagination parameters.

        Returns:
            Response: A paginated response containing the data for the current page.
                      If the page parameters are invalid, returns a JSON error response.
        """
        try:
            paginated_data = self.paginate_queryset(queryset, request)
            response = self.get_paginated_response(paginated_data)
            return JsonResponseSuccess(response.data)
        except NotFound as err:
            return JsonResponseError("Invalid page", status=400)
