from rest_framework.exceptions import APIException


class BlacklistConflictApiException(APIException):
    status_code = 409
    default_detail = "This Fibonacci number is already blacklisted."


class BlacklistNotFoundApiException(APIException):
    status_code = 404
    default_detail = "This number is not found in the blacklist."
