from fastapi import APIRouter, Query, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import List

from fastapi.param_functions import Body
from models.spammer import Spammer

from schemas import spammer as spammer_schemas
from crud import spammers
from db.session import DatabaseSession, Session, get_database_session
from spammer_connector import connect_spammer, send_spammer_command, \
            open_spammer_connection, close_spammer_connection

from os import path
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix='/spammers',
    tags=['spammers'],
)


@router.on_event("startup")
async def sync_spammer_script(
    # session: Session = Depends(get_database_session),
    # spammer_connector = Depends(connect_spammer)
    # test_val = Depends(test_dep)
):
    logger.info('spammer router startup')

    session = DatabaseSession()
    spammer_connector = await open_spammer_connection()

    database_result = spammers.read_spammers_by_ids(session, [])
    # transform orm models to pydantic models
    database_result = [spammers.spammer_from_orm(spammer) for spammer in database_result]

    logger.info('add spammers database status:' + str(database_result))

    add_status = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='replace', data=database_result
        )
    )

    logger.info('app spammers command result:' + str(add_status))

    session.close()
    await close_spammer_connection(spammer_connector)


@router.post(
    '/',
    response_model=spammer_schemas.SpammerResult,
    status_code=status.HTTP_201_CREATED
)
async def spammers_create(
    spammer_data: List[spammer_schemas.SpammerIn],
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.create_spammers(session, spammer_data)
    # transform orm models to pydantic models
    database_result = [spammers.spammer_from_orm(spammer) for spammer in database_result]
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='add', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.put('/', response_model=spammer_schemas.SpammerOut)
async def spammers_update(
    spammer_data: spammer_schemas.SpammerIn,
    id=Query(None),
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.update_spammer_by_id(session, spammer_data, id)
    result = send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='update', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.delete('/', response_model=spammer_schemas.SpammerResult)
async def spammers_delete(
    spammer_data: List[int] = Query([]),
    id=Query(None),
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.delete_spammer_by_id(session, spammer_data)
    spammers_ids = list(map(lambda m: m.id, database_result))
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='delete', data=spammers_ids
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.get('/', response_model=spammer_schemas.SpammerResult)
async def spammers_get(
    offset: int = Query(0),
    limit: int = Query(0),
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.read_spammers(session, offset, limit)
    spammers_ids = list(map(lambda m: m.id, database_result))
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='state', data=spammers_ids
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.get('/status', response_model=spammer_schemas.SpammerResult)
async def spammers_get_by_id(
    spammer_data: List[int] = Query([]),
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.read_spammers_by_ids(session, spammer_data)
    spammers_ids = list(map(lambda m: m.id, database_result))
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='state', data=spammers_ids
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.put('/start', response_model=spammer_schemas.SpammerResult)
async def spammers_start_by_id(
    spammer_data: List[int],
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.start_spammers_by_ids(session, spammer_data)
    spammers_ids = list(map(lambda m: m.id, database_result))
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='start', data=spammers_ids
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.put('/stop', response_model=spammer_schemas.SpammerResult)
async def spammers_start_by_id(
    spammer_data: List[int],
    session: Session = Depends(get_database_session),
    spammer_connector = Depends(connect_spammer)
):
    database_result = spammers.stop_spammers_by_ids(session, spammer_data)
    spammers_ids = list(map(lambda m: m.id, database_result))
    result = await send_spammer_command(
        spammer_connector,
        command=spammer_schemas.SpammerCommand(
            command='stop', data=spammers_ids
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )
