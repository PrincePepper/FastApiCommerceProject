# Sereda Semen
# 2022, 00.00

# Sereda Semen, 2022
# Роутер по работе со связями indicators

from typing import Any

from fastapi import APIRouter, Body
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api import deps
from app.models import SourcesDependencies, Sources
from app.models.users import Users as model_User
from app.schemas import SourceCreate, SourceUpdateProperties
from source_files import lab_1c

router = APIRouter()


@router.post("/update_sources")
def init_sources(
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Запустить обновление источников
    """

    def create(db: Session, obj_in):
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)

    def get_by_id(db: Session, id: str):
        return db.query(Sources).filter(Sources.id == id).first()

    lab1c = lab_1c.get_about_me()
    lab1c = SourceCreate(**lab1c)  # type: ignore
    id = get_by_id(db, id=lab1c.id)
    if not id:
        lab1c = Sources(id=lab1c.id,
                        name=lab1c.name,
                        address=lab1c.address,
                        properties=lab1c.properties)
        create(db, lab1c)
    return {'result': "ok"}


@router.post("/get_sources")
def get_sources(
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Возвращает все источники с последней датой обновления
    """
    aaa = db.query(Sources.id, Sources.name, Sources.last_update).all()
    return aaa


@router.post("/get_max_last_update_source")
def max_last_update_source(
        db: Session = Depends(deps.get_db),
        # current_user: model_User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Возвращает последнюю актуальную версию ресурсов
    """
    result = db.query(SourcesDependencies.indicator_id,
                      func.max(Sources.last_update).label(
                          "last_update")).select_from(
        Sources).join(
        SourcesDependencies,
        SourcesDependencies.source_id == Sources.id).group_by(
        SourcesDependencies.indicator_id,
        Sources.id).all()

    return result

@router.post("/get_source_by_id")
def get_source_by_id(source_id: dict = Body({"source_id": "UUID"}),
                     db: Session = Depends(deps.get_db),
                     current_user: model_User = Depends(deps.get_current_active_user),
                     ) -> Any:
    """
    Возвращает источник по id
    """
    aaa = db.query(Sources.name, Sources.address, Sources.properties).filter(
        Sources.id == source_id['source_id']).all()
    return aaa


@router.post("/get_all_indicators_for_source")
def get_all_indicators_for_source(source_id: dict = Body({"source_id": "UUID"}),
                                  db: Session = Depends(deps.get_db),
                                  current_user: model_User = Depends(deps.get_current_active_user),
                                  ) -> Any:
    """
    Возвращает все индикаторы по источнику
    """
    aaa = db.query(SourcesDependencies.indicator_id).filter(
        SourcesDependencies.source_id == source_id['source_id']).all()
    return aaa


# TODO: нужно доделать
@router.post("/set_properties")
def set_properties(payload: SourceUpdateProperties,
                   db: Session = Depends(deps.get_db),
                   current_user: model_User = Depends(deps.get_current_active_user),
                   ) -> Any:
    """
    установка параметров в источнике
    """
    print(payload)
    aaa = db.query(Sources.properties).filter(
        Sources.id == payload.id).update(
        {'properties': str(payload.properties)})
    db.commit()
    db.refresh(aaa)
    return aaa
