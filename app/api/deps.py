from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud
from app.db.session import SessionLocal
from app.models.users import Users


# def get_db() -> Generator:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db() -> Generator:
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()


class UserNotFound(Exception):
    pass


def get_current_user(db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = crud.crud_user.user.get(db, id=user_id)
        if not user:
            raise UserNotFound('0008')

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='0008')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='0003')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='0009')
    return user


def get_current_active_user(
        current_user: Users = Depends(get_current_user),
) -> Users:
    if not crud.crud_user.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="0010")
    return current_user


def get_current_active_superuser(
        current_user: Users = Depends(get_current_active_user),
) -> Users:
    if not crud.crud_user.user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="0006"
        )
    return current_user
