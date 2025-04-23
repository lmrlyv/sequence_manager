import logging
import traceback

from rest_framework.views import exception_handler

from sequence_manager.utils.constants import IS_DEBUG_ON
from sequence_manager.utils.custom_responses import JsonResponseError


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for Django REST Framework.

    This function handles exceptions raised in the application and customizes the response format.
    It ensures the consistent structure from the endpoints.
    """
    response = exception_handler(exc, context)

    if response is None:
        logger.error(traceback.format_exc())
        error_message = str(exc) if IS_DEBUG_ON else "Please contact the system administrator."
        return JsonResponseError(error_message, message="Unknown error", status=500)

    message = response.data.get("code")
    error_message = response.data["detail"] if "detail" in response.data else response.data
    return JsonResponseError(error_message, message=message, status=response.status_code)
