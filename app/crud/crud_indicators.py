from typing import Any, Optional, Union, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.indicators import Indicators, IndicatorInstance, \
    IndicatorsAccess
from app.schemas.indicators import IndicatorCreate, IndicatorUpdate, \
    IndicatorInstanceCreate, \
    IndicatorAccessCreate, IndicatorInstanceChange


def create_instance(db: Session,
                    obj_in: IndicatorInstanceCreate) -> IndicatorInstance:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = IndicatorInstance(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


class CRUDIndicators(CRUDBase[Indicators, IndicatorCreate, IndicatorUpdate]):

    def get_by_id(self, db: Session, *, id: str) -> Optional[Indicators]:
        return db.query(Indicators).filter(Indicators.id == id).first()

    def update(
            self, db: Session, *, db_obj: Indicators,
            obj_in: Union[IndicatorUpdate, Dict[str, Any]]
    ) -> Indicators:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def deleteAll(self, db: Session) -> Any:
        rows_delete = db.query(Indicators).delete()
        return {"msg": f"удалено строк - {rows_delete}"}

    def get_all_indicators(self, db: Session, id: str) -> Any:
        return db.query(IndicatorInstance.screen_number,
                        IndicatorInstance.id.label('instance_id'),
                        IndicatorInstance.properties.label(
                            'instance_properties'),
                        Indicators.diagram_type,
                        Indicators.id.label('indicator_id'),
                        Indicators.name,
                        Indicators.properties.label(
                            'indicator_properties')).select_from(
            IndicatorsAccess).filter(
            IndicatorsAccess.user_id == id) \
            .join(IndicatorInstance,
                  IndicatorInstance.indicators_access_id == IndicatorsAccess.id) \
            .join(Indicators,
                  Indicators.id == IndicatorsAccess.indicator_id).all()

    def get_all_indicators_for_user(self, db: Session, id: str) -> Any:
        return db.execute("SELECT t1.id,COALESCE(t2.is_active, false) "
                          f"FROM indicators t1 left JOIN indicators_access t2 ON t1.id = t2.indicator_id and t2.user_id='{str(id)}'").all()
        # return db.query(IndicatorsAccess.indicator_id, IndicatorsAccess.is_active).filter(
        #    IndicatorsAccess.user_id == id).all()

    def get_all_users_for_indicators(self, db: Session, id: str) -> Any:
        return db.execute("SELECT t1.id,COALESCE(t2.is_active, false) "
                          f"FROM users t1 left JOIN indicators_access t2 ON t1.id = t2.user_id and t2.indicator_id='{str(id)}'").all()

    # def get_all_users(self, db: Session, id: str) -> Any:
    #     return db.query(IndicatorsAccess.user_id, IndicatorsAccess.is_active).filter(
    #         IndicatorsAccess.indicator_id == id).all()

    def create_access(self, db: Session,
                      obj_in: IndicatorAccessCreate) -> IndicatorsAccess:
        a = CRUDBase(IndicatorsAccess).create(db=db, obj_in=obj_in)
        return a

    def get_all_access(self, db: Session, id: str) -> Any:
        return db.query(IndicatorsAccess.id.label('indicators_access_id'),
                        IndicatorsAccess.indicator_id,
                        Indicators.name.label('indicators_name'),
                        Indicators.diagram_type).select_from(
            IndicatorsAccess).filter(
            IndicatorsAccess.user_id == id) \
            .join(Indicators,
                  IndicatorsAccess.indicator_id == Indicators.id).all()

    def create_instance(self, db: Session,
                        obj_in: IndicatorInstanceCreate) -> IndicatorInstance:
        a = CRUDBase(IndicatorInstance).create(db=db, obj_in=obj_in)
        return a

    def detect(self, db: Session, obj_in: IndicatorInstanceChange):
        aaa = db.execute(
            "SELECT public.indicator_instance.id indicator_instance_id, "
            "public.indicator_instance.properties indicator_instance_properties,"
            "public.indicator_instance.screen_number,"
            "public.indicators.name,"
            "public.indicators.alias,"
            "public.indicators.diagram_type,"
            "public.indicators.properties indicators_properties,"
            "updatedindicators.last_update,"
            "public.indicators.text_sql"
            " FROM public.indicator_instance"
            " INNER JOIN public.indicators_access "
            "ON (public.indicator_instance.indicators_access_id = public.indicators_access.id)"
            " INNER JOIN public.indicators"
            " ON (public.indicators_access.indicator_id = public.indicators.id)"
            " INNER JOIN ("
            " select public.sources_dependencies.indicator_id,"
            " Max(public.sources.last_update) last_update"
            " FROM public.sources"
            " INNER JOIN public.sources_dependencies"
            " ON public.sources.id = public.sources_dependencies.source_id"
            f" WHERE public.sources.last_update > {obj_in.last_update}"
            " GROUP BY public.sources_dependencies.indicator_id) "
            "AS UpdatedIndicators "
            "ON public.indicators_access.indicator_id = UpdatedIndicators.indicator_id"
            f" WHERE public.indicators_access.user_id = '{str(obj_in.user_id)}' AND"
            " public.indicators_access.is_active AND"
            f" public.indicator_instance.screen_number = {obj_in.screen}")
        return aaa


indicator = CRUDIndicators(Indicators)
