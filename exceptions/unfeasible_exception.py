from exceptions.api_exception import ApiException
from fastapi import status

class UnfeasibleException(ApiException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)