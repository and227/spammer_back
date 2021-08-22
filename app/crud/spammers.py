from typing import List

from db.session import Session
from models.spammer import Spammer
from schemas import spammer as spammer_scheme

from copy import deepcopy
import json

import logging

FORMAT = '|%(levelname)s| %(asctime)s: %(filename)s %(funcName)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


statistics_template = {
    'current': 0,
    'total': 0
}


def spammer_from_orm(spammer: Spammer) -> spammer_scheme.SpammerStore:
    logger.info('from orm:')
    logger.info(spammer)
    logger.info(type(spammer.options))
    logger.info(type(spammer.statistics))
    logger.info(spammer.options)
    logger.info(spammer.statistics)
    return spammer_scheme.SpammerStore(
        id=spammer.id,
        script_template=spammer.script_template,
        login=spammer.login,
        password=spammer.password,
        options=spammer.options,
        state=spammer.state,
        statistics=spammer.statistics
    )


def spammer_to_orm(spammer: spammer_scheme.SpammerIn) -> Spammer:
    return Spammer(
        script_template=spammer.script_template,
        login=spammer.login,
        password=spammer.password,
        options=spammer.options,
        state=spammer.state,
        statistics=statistics_template
    )


def create_spammers(db: Session, spammers: List[spammer_scheme.SpammerIn]):
    new_spammers = [spammer_to_orm(spammer) for spammer in spammers]
    for spammer in new_spammers:
        db.add(spammer)
    db.commit()
    return new_spammers


def update_spammer_by_id(
    db: Session,
    update_spammer: spammer_scheme.SpammerIn,
    spammer_id: int
):
    update_data = update_spammer.dict()
    update_query = db \
        .query(Spammer) \
        .filter(Spammer.id == spammer_id)
    update_query.update(update_data)
    db.commit()
    update_spammer = update_query.one()

    return update_spammer


def delete_spammer_by_id(
    db: Session,
    spammer_ids: int
):
    read_spammers_by_ids(db, spammer_ids)
    if spammer_ids:
        delete_spammers = db \
            .query(Spammer) \
            .filter(Spammer.id.in_(spammer_ids))
    else:
        delete_spammers = db.query(Spammer)
    ret_spammers = deepcopy(delete_spammers.all())
    delete_spammers.delete(synchronize_session=False)
    db.commit()
    return ret_spammers


def read_spammers(
    db: Session,
    offset: int = 0,
    limit: int = 10
):
    return db.query(Spammer) \
        .order_by(Spammer.id) \
        .offset(offset) \
        .limit(limit) \
        .all()


def read_spammers_by_ids(
    db: Session,
    spammer_ids: List[int] = None
):
    if spammer_ids:
        result = db \
            .query(Spammer) \
            .filter(Spammer.id.in_(spammer_ids)) \
            .order_by(Spammer.id) \
            .all()
    else:
        result = db \
            .query(Spammer) \
            .order_by(Spammer.id) \
            .all()
    return result


def start_spammers_by_ids(
    db: Session,
    spammer_ids: List[int] = None
):
    if spammer_ids:
        result = db \
            .query(Spammer) \
            .filter(Spammer.id.in_(spammer_ids)) \
            .update({
                'state': spammer_scheme.SpammerStateEnum.working
            }, synchronize_session=False)
    else:
        result = db \
            .query(Spammer) \
            .update({
                'state': spammer_scheme.SpammerStateEnum.working
            }, synchronize_session=False)
    db.commit()
    return read_spammers_by_ids(db, spammer_ids)


def stop_spammers_by_ids(
    db: Session,
    spammer_ids: List[int] = None
):
    if spammer_ids:
        result = db \
            .query(Spammer) \
            .filter(Spammer.id.in_(spammer_ids)) \
            .update({
                'state': spammer_scheme.SpammerStateEnum.stopped
            }, synchronize_session=False)
    else:
        result = db \
            .query(Spammer) \
            .update({
                'state': spammer_scheme.SpammerStateEnum.stopped
            }, synchronize_session=False)
    db.commit()
    return read_spammers_by_ids(db, spammer_ids)

