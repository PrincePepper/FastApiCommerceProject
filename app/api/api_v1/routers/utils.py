import datetime

from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
from sqlalchemy import create_engine

from app.core.config import settings

router = APIRouter()


@router.on_event("startup")
@repeat_every(seconds=1 * 1)  # 1 minute
def save_1clab_database():  # раз в час подгружает данные с 1cLAB
    current_datetime = datetime.datetime.now().timetuple()
    # begin = f'{current_datetime.tm_year}-{current_datetime.tm_mon}-{current_datetime.tm_mday}T01:01:01'
    begin = f'2022-01-01T01:01:01'
    end = f'{"{:02}".format(current_datetime.tm_year)}-{"{:02}".format(current_datetime.tm_mon)}-{"{:02}".format(current_datetime.tm_mday)}T{"{:02}".format(current_datetime.tm_hour)}:{"{:02}".format(current_datetime.tm_min)}:{"{:02}".format(current_datetime.tm_sec)}'

    from sqlalchemy.orm import sessionmaker
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    # res = get_api_1clab(begin_date=begin, end_date=end, db=db)
    # print(res)
