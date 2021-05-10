from fastapi import APIRouter, Query, Depends
from typing import List

from schemas import spammer
from crud import spammers
from db.session import Session, get_database_session

router = APIRouter(
    prefix='/spammers',
    tags=['spammers'],
)

@router.get('/', response_model=List[spammer.SpammerOut])
async def spammers_get(
        offset: int = Query(0),
        limit: int = Query(0),
        session: Session = Depends(get_database_session)
    ):
    return spammers.read_spammers(session, offset, limit)

@router.post('/', response_model=spammer.SpammerOut)
async def spammers_create(
        spammer: spammer.SpammerIn,
        session: Session = Depends(get_database_session)
    ):
    return spammers.create_spammer(session, spammer)