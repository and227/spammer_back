from db.session import Session
from models.user import UserTable
from schemas import user as user_scheme
from core.helpers import pass_context

def create_user(db: Session, user: user_scheme.UserIn):
    new_user = UserTable(
        email=user.email,
        hashed_password=pass_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    result = db.query(UserTable) \
        .filter(UserTable.email == email) \
        .first()
    return result
