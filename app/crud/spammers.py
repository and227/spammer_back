from db.session import Session
from models.spammer import Spammer
from schemas import spammer as spammer_scheme

def read_spammers(db: Session, offset: int = 0, limit: int = 10):
    return db.query(Spammer).offset(offset).limit(limit).all()

def read_spammer_by_id(db: Session, spammer_id: int = None):
    return db \
        .query(Spammer) \
        .filter(Spammer.spammer_id == id) \
        .first()

def create_spammer(db: Session, spammer: spammer_scheme.SpammerIn):
    new_spammer = Spammer(
        name=spammer.name,
        target=spammer.target
    )
    db.add(new_spammer)
    db.commit()
    db.refresh(new_spammer)
    return new_spammer