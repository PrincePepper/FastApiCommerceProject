# Sereda Semen, 2022
# Роутер по логинизации и получении токена и обновления токена


from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api import deps
from app.core.config import settings
from app.schemas import UserAccess

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRE_MINUTES


@router.post('/access')
def login(payload: UserAccess,
          db: Session = Depends(deps.get_db),
          Authorize: AuthJWT = Depends()):
    """
    Отвечает за авторизацию пользователя и сохранения в куки refresh и access токена

    :param payload: входные данные - почта и пароль\n
    :return: возвращает токен
    """
    user = crud.user.authenticate(
        db, email=payload.email, password=payload.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='0001')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {'access_token': access_token,
            'refresh_token': refresh_token}


@router.post('/refresh')
def refresh_token(response: Response,
                  request: Request,
                  db: Session = Depends(deps.get_db),
                  Authorize: AuthJWT = Depends()):
    """
    Отвечает за обновление access токена\n
    :return: ничего не возвращает, только обновляет куки
    """
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='0002')
        user = crud.user.get_by_id(db, id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='0003')
        access_token = Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Предоставьте токен обновления')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    Authorize.set_access_cookies(access_token)

    return {'access_token': access_token}


@router.post('/logout', status_code=status.HTTP_200_OK)
def logout(Authorize: AuthJWT = Depends(),
           user_id: str = Depends(deps.get_current_user)):
    """
    Выкинуть из авторизации пользователя
    """
    Authorize.unset_jwt_cookies()
    Authorize.unset_refresh_cookies()

    return {'detail': 'success'}

