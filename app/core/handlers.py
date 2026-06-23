from app.core.exceptions import ApiException
from app.core.responses import ApiError
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi import status


async def api_exception_handler(request: Request, exc: ApiException):
    """
    Handle business logic exceptions
    """

    return ApiError(
        message=exc.detail.get("message", "Something went wrong"),
        status_code=exc.status_code,
        details=exc.detail.get("details"),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors and format nicely
    """

    # Construct first error message including the field
    errors = exc.errors()
    if errors:
        loc = errors[0]["loc"]
        # Extract the actual field name
        field_name = loc[-1] if len(loc) > 1 else loc[0]
        first_error_msg = f"{field_name} {errors[0]['msg']}"
    else:
        first_error_msg = "Invalid input"

    return ApiError(
        message=first_error_msg,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=errors,
    )
