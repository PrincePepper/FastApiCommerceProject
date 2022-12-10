# Sereda Semen, 2022
# Роутер по работе напрямую с параметрами базы данных
import subprocess
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import main
from app.api import deps
from app.api.deps import get_db
from app.core.config import settings
from app.db import session
from app.schemas.database_properties import DatabaseInfo, DatabaseGetInfo
from app.schemas.utils import Msg

# Sereda Semen, 2022
# Роутер по работе со связями database

router = APIRouter()


@router.post("/update_database_info",
             response_model=Msg)
def update_database_info(data: DatabaseInfo) -> Any:
    """
    Обновление ссылки на подключение к базе данных
    """
    str_url = f'postgresql://{data.username}:{data.password}@{data.host}:{data.port}/{data.db}'
    engine = create_engine(str_url, pool_pre_ping=True)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        # Попытка создать сессию к базе данных
        db = session_local()
        db.execute("SELECT 1")
    except Exception as e:
        raise HTTPException(
            status_code=404, detail="0007"
        )
    settings.POSTGRES_SERVER_HOST = data.host
    settings.POSTGRES_SERVER_PORT = data.port
    settings.POSTGRES_USERNAME = data.username
    settings.POSTGRES_PASSWORD = data.password
    settings.POSTGRES_DATABASE = data.db
    settings.SQLALCHEMY_DATABASE_URI = str_url

    session.SessionLocal.configure(bind=engine)

    def override_get_db():
        global db
        try:
            db = session.SessionLocal()
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    subprocess.check_call(f'dotenv -q never set POSTGRES_SERVER_HOST {data.host}')
    subprocess.check_call(f'dotenv -q never set POSTGRES_SERVER_PORT {data.port}')
    subprocess.check_call(f'dotenv -q never set POSTGRES_USERNAME {data.username}')
    subprocess.check_call(f'dotenv -q never set POSTGRES_PASSWORD {data.password}')
    subprocess.check_call(f'dotenv -q never set POSTGRES_DATABASE {data.db}')
    subprocess.check_call(f'dotenv -q never set SQLALCHEMY_DATABASE_URI {str_url}')
    return {"detail": "Информация на базу данных обновлена"}


@router.post("/get_database_info", response_model=DatabaseGetInfo)
def get_database_info():
    str_url = f'postgresql://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}' \
              f'@{settings.POSTGRES_SERVER_HOST}:{settings.POSTGRES_SERVER_PORT}/{settings.POSTGRES_DATABASE}'
    engine = create_engine(str_url, pool_pre_ping=True)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        # Попытка создание сессии БД если она поднята
        db = session_local()
        db.execute("SELECT 1")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404, detail="0007"
        )

    temp_list_db = db.execute(
        "select datname from pg_database where not datname = 'postgres' and datname not like 'temp%'").all()
    list_db = []
    for i in temp_list_db:
        list_db.append(i[0])

    result = {
        'host': settings.POSTGRES_SERVER_HOST,
        'port': settings.POSTGRES_SERVER_PORT,
        'username': settings.POSTGRES_USERNAME,
        'password': settings.POSTGRES_PASSWORD,
        'db': settings.POSTGRES_DATABASE,
        'list_db': list_db
    }
    return result


@router.post('/health_check',
             response_model=Msg)
async def get_version_database(db: Session = Depends(deps.get_db)):
    """
    Возвращает актуальную версию базы данных
    """
    try:
        db.execute("SELECT 1")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404, detail="0007"
        )
    return {'detail': 'ok'}
