from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from pydantic import BaseModel

from schemas.user import UserIn
from schemas.token import Token
from core.config import settings

from redis import Redis
from datetime import timedelta

router = APIRouter(tags=['authentication'])

redis_denylist = Redis(
    host=settings.REDIS_SERVER,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DATABASE_NUM,
    password=settings.REDIS_PASSWORD)

class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET
    authjwt_algorithm: str = settings.JWT_ALGO
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}

@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()

@AuthJWT.token_in_denylist_loader
def check_token_in_denylist(token):
    is_revoked = redis_denylist.get(token['jti'])
    return is_revoked and is_revoked == True

def create_token_pair(Authorization: AuthJWT, subj: str) -> Token:
    access_token = Authorization.create_access_token(
        subject=subj,
        expires_time=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    refresh_token = Authorization.create_refresh_token(
        subject=subj,
        expires_time=timedelta(
            minutes=settings.REFRESH_TOKER_EXPIRE_MINUTES
        )
    )
    saved_token = access_token
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post('/register', response_model=Token)
async def register(user: UserIn, Authorization: AuthJWT = Depends()):
    if user.email == settings.USER_LOGIN \
        and user.password == settings.USER_PASSWORD:
        return create_token_pair(Authorization, user.email)

@router.post('/refresh')
async def login(Authorization: AuthJWT = Depends()):
    # add previous access jwt token to denylist
    denylist.add(Authorization.get_raw_jwt(saved_token)['jti'], 10, True)
    Authorization.jwt_refresh_token_required()
    # add previous refresh jwt token to denylist 
    redis_denylist.setex(Authorization.get_raw_jwt()['jti'], 10, True)

    subject = Authorization.get_jwt_subject()
    return create_token_pair(subject)

