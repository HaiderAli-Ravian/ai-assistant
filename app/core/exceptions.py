from fastapi import HTTPException
from fastapi import status


class ApiException(HTTPException):
    """
    Custom exception class for business logic errors.
    """

    def __init__(
        self, message: str, details=None, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(
            status_code=status_code, detail={"message": message, "details": details}
        )
