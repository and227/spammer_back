from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, RevokedTokenError
from fastapi import status

from pydantic import BaseModel
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from schemas.user import UserIn, UserInRegister
from schemas.token import Token
from core.config import settings
from db.session import Session, get_database_session
from crud import users

from redis import Redis
from datetime import timedelta
from core.helpers import pass_context

from os import path
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

router = APIRouter(tags=['authentication'])

redis_denylist = Redis(
        host=settings.REDIS_SERVER,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DATABASE_NUM,
        # password=settings.REDIS_PASSWORD
    )

class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET
    authjwt_algorithm: str = settings.JWT_ALGO
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    access_expires: int = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires: int = timedelta(minutes=settings.REFRESH_TOKER_EXPIRE_MINUTES)

auth_jwt_settings = AuthJWTSettings()


@AuthJWT.load_config
def get_config():
    return auth_jwt_settings


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(token):
    token_id = token['jti']
    token_type = token['type']
    is_revoked = redis_denylist.get(token_id)
    if is_revoked:
        result = is_revoked.decode() == 'true'
    else:
        result = False
    logger.info(f'checking {token_type} token {token_id} with value "{is_revoked}"; resuld - {result}')
    return result


def create_token_pair(Authorization: AuthJWT, subj: str) -> Token:
    access_token = Authorization.create_access_token(
        subject=subj
    )
    refresh_token = Authorization.create_refresh_token(
        subject=subj
    )
    redis_denylist.set('saved_token', access_token)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


def authenticate_user(session: Session, user: UserIn):
    db_user = users.get_user_by_email(session, user.email)
    if db_user:
        if pass_context.verify(user.password, db_user.hashed_password):
            return True
        else:
            return False
    else:
        return False


@router.post('/register', response_model=Token)
async def register(
        user: UserInRegister,
        Authorization: AuthJWT = Depends(),
        session: Session = Depends(get_database_session),
    ):
    if not users.get_user_by_email(session, user.email):
        users.create_user(session, user)
        return create_token_pair(Authorization, user.email)
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Email must be unique.'
        )

@router.post('/login', response_model=Token)
async def register(
        user: UserIn,
        Authorization: AuthJWT = Depends(),
        session: Session = Depends(get_database_session),
    ):
    if authenticate_user(session, user):
        return create_token_pair(Authorization, user.email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='wrong email or password',
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post('/refresh')
async def login(Authorization: AuthJWT = Depends()):
    # add previous access jwt token to denylist
    saved_token = redis_denylist.get('saved_token')
    redis_denylist.setex(
        Authorization.get_raw_jwt(saved_token)['jti'],
        settings.ACCESS_TOKEN_EXPIRE_MINUTES*60, 'true'
    )
    Authorization.jwt_refresh_token_required()
    # add previous refresh jwt token to denylist 
    redis_denylist.setex(
        Authorization.get_raw_jwt()['jti'],
        settings.REFRESH_TOKER_EXPIRE_MINUTES*60, 'true'
    )

    subject = Authorization.get_jwt_subject()
    return create_token_pair(Authorization, subject)


@router.get('/access')
async def access_test(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        token_id = Authorization.get_raw_jwt()['jti']
        logger.info(f'autorization passed with {token_id}')
        return {'status': 'OK'}
    except RevokedTokenError as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
