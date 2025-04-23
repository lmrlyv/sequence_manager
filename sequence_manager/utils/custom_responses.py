from typing import Any

from django.http import JsonResponse


class JsonResponseSuccess(JsonResponse):
    """
    Custom response class for successful requests.

    This class is used to return a JSON response indicating a successful operation.
    The response includes a success flag, and associated data object, and an optional message.

    Attributes:
        data (Any): A JSON-serializable object containing data.
        message (str, optional): A message describing the success of the operation. If not
            provided, it will be omitted from the response by default.

    Example Usage:
        JsonResponseSuccess({"key": "value"})
    """

    def __init__(self, data, *args, message=None, **kwargs):
        data = {"success": True, "data": data}
        super().__init__(data, *args, **kwargs)


class JsonResponseError(JsonResponse):
    """
    Custom response class for error responses.

    This class is used to return a JSON response indicating an error.
    The response includes a failure flag, an error object, and an optional message.

    Attributes:
        error (Any): A JSON-serializable object containing error details.
        message (str, optional): A message describing the error that occurred. If not provided, it
            will be omitted from the response by default.

    Example Usage:
        JsonResponseError("Validation failed")
    """

    def __init__(self, error, *args, message=None, **kwargs):
        data = {"success": False, "error": error}

        if message is not None:
            data["message"] = message

        super().__init__(data, *args, **kwargs)
