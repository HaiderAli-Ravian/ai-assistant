from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ApiResponse(JSONResponse):
    """Standard success response"""

    def __init__(
        self,
        data: Any = None,
        message: str = "Success",
        status_code: int = 200,
    ):
        content = jsonable_encoder({
            "success": True,
            "message": message,
            "data": data,
        })
        super().__init__(status_code=status_code, content=content)


class ApiError(JSONResponse):
    """Standard error response"""

    def __init__(
        self,
        message: str = "Something went wrong",
        status_code: int = 400,
        details: Optional[Any] = None,
    ):
        content = jsonable_encoder({
            "success": False,
            "message": message,
            "error": {
                "code": status_code,
                "details": details,
            },
        })
        super().__init__(status_code=status_code, content=content)
