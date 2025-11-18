import logging
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from exceptions.api_exception import ApiException, api_exception_handler
from routers import plant

#should be /api or /api/v1, but to comply with the challenge requirements, it is left empty
prefix = ""

app = FastAPI(
    title="Powerplant SMT API",
    description="API for managing powerplant data in the SMT system. Coding Challenge for ENGIE.",
    version="1.0.0",
    docs_url= prefix + "/docs",
    redoc_url= prefix + "/redoc",
)

app.add_exception_handler(ApiException, api_exception_handler)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    json_exc = JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "exception_case": exc.__class__.__name__,
            "detail": str(exc)
        },
    )
    logging.error(f"Unhandled Exception: {exc}", exc_info=True)
    return json_exc

api_router = APIRouter(prefix=prefix)

api_router.include_router(plant.router)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)