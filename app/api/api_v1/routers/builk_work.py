# Sereda Semen, 2022
# Роутер по работе со связями builk work

from typing import Any

from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.users import Users as model_User

router = APIRouter()


@router.post("/multi_sql_all")
def multi_sql_all(
        sql: dict = Body({"sql": "string"}),
        db: Session = Depends(deps.get_db),
        current_user: model_User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Делает запрос в базу данных по SQL запросу, который возвращает все данные
    """
    try:
        result = db.execute(sql['sql']).all()
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e))
    return {"data": result}
