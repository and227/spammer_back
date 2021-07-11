from typing import List

from db.session import Session
from models.spammer import Spammer
from schemas import spammer as spammer_scheme

def spammer_from_orm(spammer: Spammer) -> spammer_scheme.SpammerStore:
    return spammer_scheme.SpammerStore(
        id=spammer.id,
        spammer_type=spammer.spammer_type,
        login=spammer.login,
        state=spammer.state,
        target=spammer_scheme.SpammerTarget(
            target_type=spammer.target_type,
            current=spammer.current,
            total=spammer.total
        )
    )

def create_spammers(db: Session, spammers: List[spammer_scheme.SpammerIn]):
    new_spammers = [Spammer(
        spammer_type=spammer.spammer_type,
        login=spammer.login,
        target_type=spammer.target.target_type,
        current=spammer.target.current,
        total=spammer.target.total
    ) for spammer in spammers]
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
    update_data.update(update_data['target'])
    del update_data['target']

    update_spammer = db.query(Spammer) \
        .filter(Spammer.id == spammer_id) \
        .first()
    for spammer in update_spammer:
        spammer.update(update_data)
    db.commit()
    db.refresh(update_spammer)
    return update_spammer


def delete_spammer_by_id(
    db: Session,
    spammer_id: int
):
    delete_spammer = db.query(Spammer) \
        .filter(Spammer.id == spammer_id) \
        .first()
    if delete_spammer:
        db.delete(delete_spammer)
    db.commit()
    return delete_spammer


def read_spammers(
    db: Session,
    offset: int = 0,
    limit: int = 10
):
    return db.query(Spammer).offset(offset).limit(limit).all()


def read_spammers_by_ids(
    db: Session,
    spammer_ids: List[int] = None
):
    if spammer_ids:
        result = db \
            .query(Spammer) \
            .filter(Spammer.id.in_(spammer_ids)) \
            .all()
    else:
        result = db \
            .query(Spammer) \
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

