from fastapi import APIRouter, Query, Depends
from fastapi.exceptions import HTTPException
from typing import List

from fastapi.param_functions import Body

from schemas import spammer as spammer_schemas
from crud import spammers
from db.session import Session, get_database_session
from spammer_connector import connect_spammer_socket, send_spammer_command

router = APIRouter(
    prefix='/spammers',
    tags=['spammers'],
)


@router.post('/', response_model=spammer_schemas.SpammerOut)
async def spammers_create(
    spammer_data: List[spammer_schemas.SpammerIn],
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.create_spammers(session, spammer_data)
    result = send_spammer_command(
        spammer_socket,
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
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.update_spammer_by_id(session, spammer_data, id)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='update', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.delete('/', response_model=spammer_schemas.SpammerOut)
async def spammers_delete(
    id=Query(None),
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.delete_spammer_by_id(session, id)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='delete', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.get('/', response_model=List[spammer_schemas.SpammerOut])
async def spammers_get(
    offset: int = Query(0),
    limit: int = Query(0),
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.read_spammers(session, offset, limit)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='status', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.get('/status', response_model=List[spammer_schemas.SpammerOut])
async def spammers_get_by_id(
    spammer_data: List[int],
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.read_spammers_by_ids(session, spammer_data)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='status', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.put('/start', response_model=List[spammer_schemas.SpammerOut])
async def spammers_start_by_id(
    spammer_data: List[int],
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.start_spammers_by_ids(session, spammer_data)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='start', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )


@router.put('/stop', response_model=List[spammer_schemas.SpammerOut])
async def spammers_start_by_id(
    spammer_data: List[int],
    session: Session = Depends(get_database_session),
    spammer_socket = Depends(connect_spammer_socket)
):
    database_result = spammers.stop_spammers_by_ids(session, spammer_data)
    result = send_spammer_command(
        spammer_socket,
        command=spammer_schemas.SpammerCommand(
            command='stop', data=database_result
        )
    )
    return spammer_schemas.SpammerResult(
        status='success',
        data=result
    )
