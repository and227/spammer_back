from main import app
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(AuthJWTException)
def auth_jwt_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.message }
        )