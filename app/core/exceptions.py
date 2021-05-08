from main import app
from fastapi_jwt_auth.exceptions import AuthJWTException

@app.exception_handler(AuthJWTException)
def auth_jwt_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.message }
        )