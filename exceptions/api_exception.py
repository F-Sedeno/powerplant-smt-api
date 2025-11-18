from fastapi.responses import JSONResponse

class ApiException(Exception):
    def __init__(self, detail: str, status_code: int = 409):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.detail = detail
    
    def __str__(self):
        return f"ApiException(status_code={self.status_code}, detail={self.detail})"

async def api_exception_handler(request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "exception_case": exc.exception_case,
            "detail": exc.detail
        },
    )