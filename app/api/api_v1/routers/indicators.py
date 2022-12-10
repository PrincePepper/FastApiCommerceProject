# Sereda Semen, 2022
# Роутер по работе со связями indicators

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.api_v1.routers.builk_work import multi_sql_all
from app.api.api_v1.routers.source import max_last_update_source
from app.api.api_v1.routers.user import update_user
from app.models.users import Users as model_User
from app.schemas import UserIndicatorStatus
from app.schemas.indicators import Indicator as schemas_Indicators, \
    IndicatorInstance as schemas_IndicatorInstance, \
    IndicatorInstanceChange, IndicatorCreate, IndicatorAllInformation, \
    IndicatorsAccessInformation, IndicatorAccessUpdateStatus
from app.schemas.indicators import IndicatorUpdate, IndicatorAccessCreate, \
    IndicatorInstanceCreate

router = APIRouter()


@router.post("/get_all_full_indicators",
             response_model=List[schemas_Indicators])
def get_all_full_indicators(
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Отдаст полный список индикаторов
    """
    indicators = crud.indicator.get_all(db)
    return indicators


@router.post("/get_all_data_for_indicator", response_model=IndicatorAllInformation)
def get_all_data_for_indicator(indicator_id: dict = Body({"indicator_id": "id"}),
                               db: Session = Depends(deps.get_db),
                               current_user: model_User = Depends(deps.get_current_active_user),
                               ) -> Any:
    """
    Отдает структуру данного по одному индикатору
    """
    indicator = crud.indicator.get_by_id(db, id=indicator_id["indicator_id"])
    update = max_last_update_source(db=db)
    for i in update:
        if i[0] == indicator.id:
            update = i[1]
            break
    aaa = multi_sql_all(sql={"sql": indicator.text_sql}, db=db, current_user=current_user)  # name, value
    names = []
    values = []
    for i in aaa['data']:
        names.append(i[0])
        values.append([i[1]])

    screen_and_properties = db.execute("SELECT indicator_instance.screen_number,indicator_instance.properties "
                                       "FROM "
                                       "indicators_access "
                                       "INNER JOIN indicator_instance "
                                       "ON (indicators_access.id = indicator_instance.indicators_access_id)"
                                       " WHERE "
                                       "indicator_instance.indicators_access_id = indicators_access.id AND "
                                       f"indicators_access.indicator_id = '{indicator.id}' ").all()
    datasets = []
    for i in screen_and_properties:
        bbb = {
            "screen": i[0],
            **i[1],
            "data": values,
        }
        datasets.append(bbb)

    result = {
        "indicator_id": indicator.id,
        "last_update": update,
        "labels": names,
        "datasets": datasets,
        "title": "Первый график",
    }
    return result


@router.post("/get_all_indicators_for_user", response_model=List)
def get_all_indicators_for_user(user_id: dict = Body({"user_id": "UUID"}),
                                db: Session = Depends(deps.get_db),
                                current_user: model_User = Depends(deps.get_current_active_superuser),
                                ) -> Any:
    """
    Получение всех индикаторов и экранов привязанных к пользователю
    (Получить все показатели с указанием доступности для данного пользователя)
    """
    user_id = user_id['user_id']
    try:
        UUID(user_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )
    full_indicator_instance = crud.indicator.get_all_indicators_for_user(db, id=user_id)
    return full_indicator_instance


@router.post("/get_all_users_for_indicator", response_model=List)
def get_all_users_for_indicator(indicator_id: dict = Body({"indicator_id": "UUID"}),
                                db: Session = Depends(deps.get_db),
                                current_user: model_User = Depends(deps.get_current_active_superuser),
                                ) -> Any:
    """
    Получиь список всех пользователей с указанием доступа к данному показателю
    """
    indicator_id = indicator_id['indicator_id']
    try:
        UUID(indicator_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )
    list_users = crud.indicator.get_all_users_for_indicators(db, id=indicator_id)
    return list_users


@router.post("/save_indicator", response_model=schemas_Indicators)
def save_indicator(payload: IndicatorCreate,
                   db: Session = Depends(deps.get_db),
                   current_user: model_User = Depends(deps.get_current_active_superuser),
                   ) -> Any:
    """
    Схранение индикатора в базе данных
    """
    indicators = crud.indicator.create(db, obj_in=payload)
    return indicators


@router.post("/update_indicator", response_model=schemas_Indicators)
def update_indicator(payload: IndicatorUpdate,
                     indicator_id=Body(),
                     db: Session = Depends(deps.get_db),
                     current_user: model_User = Depends(deps.get_current_active_superuser),
                     ) -> Any:
    """
    Схранение индикатора в базе данных
    """

    try:
        UUID(indicator_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )

    indicator = crud.indicator.get(db, id=indicator_id)
    indicator = crud.indicator.update(db, db_obj=indicator, obj_in=payload)
    return indicator


@router.post("/get_indicator_access", response_model=IndicatorsAccessInformation)
def get_indicator_access(user_id: dict = Body({"user_id": "UUID"}),
                         db: Session = Depends(deps.get_db),
                         current_user: model_User = Depends(deps.get_current_active_user),
                         ) -> Any:
    """
    Какие на данный момент принадлежат indicator access(даже если они выключены)
    """
    user_id = user_id['user_id']
    try:
        UUID(user_id, version=4)
    except:
        raise HTTPException(
            status_code=404,
            detail="0005",
        )
    indicators = crud.indicator.get_all_access(db, id=user_id)
    return indicators


@router.post("/save_indicator_access")
def save_indicator_access(payload: IndicatorAccessCreate,
                          db: Session = Depends(deps.get_db),
                          current_user: model_User = Depends(deps.get_current_active_superuser),
                          ) -> Any:
    """
    Сохранение access в базу данных
    """
    print(payload)
    aaa = db.execute("insert into indicators_access (indicator_id,user_id, is_active ) "
                     "values "
                     f"(cast('{str(payload.indicator_id)}' as uuid),"
                     f" cast('{str(payload.user_id)}'as uuid), "
                     f"'{str(payload.is_active)}')"
                     " on conflict (indicator_id,user_id) "
                     f"do update set is_active = '{str(payload.is_active)}';")
    db.commit()
    # indicators = crud.indicator.create_access(db, obj_in=payload)
    return aaa


@router.post("/update_access_active_status", response_model=List[UserIndicatorStatus])
async def update_access_active_status(payload: IndicatorAccessUpdateStatus,
                                      db: Session = Depends(deps.get_db),
                                      current_user: model_User = Depends(deps.get_current_active_superuser)
                                      ) -> Any:
    """
    Обновление и сохранения статуса между связеми
    """
    for user in payload.users:
        db.execute("insert into indicators_access (indicator_id,user_id, is_active ) "
                   "values "
                   f"(cast('{str(payload.indicator_id)}' as uuid),"
                   f" cast('{str(user)}'as uuid), '{str(payload.users[user])}')"
                   " on conflict (indicator_id,user_id) "
                   f"do update set is_active = '{str(payload.users[user])}';")
    db.commit()
    return get_all_users_for_indicator(db=db, indicator_id={"indicator_id": str(payload.indicator_id)})


@router.post("/save_indicator_instance",
             response_model=schemas_IndicatorInstance)
def save_indicator_instance(payload: IndicatorInstanceCreate,
                            db: Session = Depends(deps.get_db),
                            current_user: model_User = Depends(deps.get_current_active_user),
                            ) -> Any:
    """
    Схранение индикаторов в базу в базу данных
    """

    indicators = crud.indicator.create_instance(db, obj_in=payload)
    indicators.properties = str(indicators.properties)
    return indicators


@router.post("/get_detect_changes")
def get_detect_changes(payload: IndicatorInstanceChange,
                       db: Session = Depends(deps.get_db),
                       current_user: model_User = Depends(
                           deps.get_current_active_user),
                       ) -> Any:
    """
    Получить список изменившихся инстансов индикаторов
    """

    indicators = crud.indicator.detect(db, obj_in=payload).all()
    return str(indicators)


@router.post("/set_from_data")
def get_detect_changes(id=Body(),
                       email=Body(),
                       name=Body(),
                       number=Body(),
                       data=Body(),
                       db: Session = Depends(deps.get_db),
                       current_user: model_User = Depends(
                           deps.get_current_active_user),
                       ) -> Any:
    """
    Получить список изменившихся инстансов индикаторов
    """
    aaa = update_user(db=db,
                      user_id=id,
                      email=email,
                      name=name,
                      phone_number=number,
                      password=None)
    for i in data:
        indicator_id, is_active = i
        payload = IndicatorAccessCreate(user_id=id, indicator_id=indicator_id, is_active=is_active)
        save_indicator_access(db=db, payload=payload)
    return {'detail': "ok"}
