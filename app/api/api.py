from fastapi import APIRouter

from api.routers import auth, users, spammers

router = APIRouter(prefix='/api')

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(spammers.router)
