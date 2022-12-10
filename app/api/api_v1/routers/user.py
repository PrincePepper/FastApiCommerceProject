# Sereda Semen, 2022
# Роутер по работе с CRUD функциями над пользователем
from operator import attrgetter
from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends, Body
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.users import Users as model_User
from app.schemas.users import User as schemas_User, UserCreate, UserUpdate, UserBase
from app.schemas.utils import DefaultBodyResponse

router = APIRouter()


@router.post("/get_users", response_model=List[schemas_User])
def read_users(
        skip: int = Body(0),
        count: int = Body(0),
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить пользователей в диапозоне от a до b. Если b = 0, то выдаст всех пользователей

    :param skip: начало поиска \n
    :param count: сколько искать \n
    :return: получение актуального списка пользователей
    """
    if count == 0:
        users = crud.crud_user.user.get_all(db)
    else:
        users = crud.crud_user.user.get_multi(db, skip=skip, limit=count)
    return sorted(users, key=attrgetter('name', 'email'))


@router.post("/create", response_model=schemas_User)
def create_user(
        user_in: UserCreate,
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Создать нового пользователя. Это может делать только администратор

    :param user_in: принимает на вход модель UserCreate(email[EmailStr],
                                                        password[str],
                                                        phone_number[Optional[str]],
                                                        is_admin[bool],
                                                        name[Optional[str]],
                                                        country_code[int])\n
    :return: Возвращает созданного пользователя в полной стуктуре
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="0004",
        )
    user_in.email = user_in.email.lower()
    user_in.name = user_in.name.replace('Ё', 'Е').replace('ё', 'е')
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.post("/update", response_model=DefaultBodyResponse)
def update_user(
        payload: UserUpdate,
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Обновление профиля. Или все сразу или по отдельности

    :return: вернет обновленного пользователя
    """
    try:
        UUID(payload.user_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )

    user = crud.user.get(db, id=payload.user_id)

    current_user_data = jsonable_encoder(user)
    user_in = UserUpdate(**current_user_data)
    if payload.password is not None:
        user_in.password = payload.password
    if payload.name is not None:
        user_in.name = payload.name
    if payload.email is not None:
        user_in.email = payload.email
    if payload.phone_number is not None:
        user_in.phone_number = payload.phone_number
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.post("/get_me", response_model=schemas_User)
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить под кем сейчас авторизован

    :return: возвращает модель User о себе
    """
    return current_user


@router.post("/find_by_name", response_model=List[schemas_User])
async def read_users_by_name(
        name: dict = Body({"name": "string"}),
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_user),
) -> List:
    """
    Поиск пользователей по подстроке ФИО

    :param name: строка по которой будет искаться пользователей \n
    :return: возвращает список пользователелей по найденому ФИО
    """
    users = crud.crud_user.user.get_similar_users(db, name=name['fullname'].lower())
    return users


@router.post("/find_by_id", response_model=schemas_User)
async def read_user_by_id(
        user_id: dict = Body({"user_id": "UUID"}),
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Получить конкретного пользователя по id.

    :param user_id: id пользователя кого мы хотим найти\n
    :return: возвращает найденного пользователя или что нет такого в системе
    """
    user_id = user_id['user_id']
    try:
        UUID(user_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )

    user = crud.user.get(db, id=user_id)
    return user
