from typing import List

from db.session import Session
from models.spammer import Spammer
from schemas import spammer as spammer_scheme


def create_spammer(db: Session, spammer: spammer_scheme.SpammerIn):
    new_spammer = Spammer(
        spammer_type=spammer.spammer_type,
        login=spammer.login,
        target=spammer.target,
        target_type=spammer.target_type
    )
    db.add(new_spammer)
    db.commit()
    db.refresh(new_spammer)
    return new_spammer


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
        .first() \
        .update(update_data)
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
    delete_spammer.delete()
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
            .filter(Spammer.id in spammer_ids) \
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
            .filter(Spammer.id in spammer_ids) \
            .all() \
            .update({
                'state': spammer_scheme.SpammerStateEnum.working
            })
    else:
        result = db \
            .query(Spammer) \
            .all() \
            .update({
                'state': spammer_scheme.SpammerStateEnum.working
            })
    return result


def stop_spammers_by_ids(
    db: Session,
    spammer_ids: List[int] = None
):
    if spammer_ids:
        result = db \
            .query(Spammer) \
            .filter(Spammer.id in spammer_ids) \
            .all() \
            .update({
                'state': spammer_scheme.SpammerStateEnum.stopped
            })
    else:
        result = db \
            .query(Spammer) \
            .all() \
            .update({
                'state': spammer_scheme.SpammerStateEnum.stopped
            })
    return result
