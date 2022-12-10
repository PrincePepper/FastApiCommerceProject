from typing import Any, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.builk_works import BuilkWorks
from app.schemas.builk_works import BuilkWorkCreate, BuilkWorkUpdate


class CRUDBuilkWork(CRUDBase[BuilkWorks, BuilkWorkCreate, BuilkWorkUpdate]):

    def get_by_id(self, db: Session, *, id: str) -> Optional[BuilkWorks]:
        return db.query(BuilkWorks).filter(BuilkWorks.id == id).first()

    def create(self, db: Session, *, obj_in: BuilkWorkCreate) -> BuilkWorks:
        db_obj = BuilkWorks(
            data_time=obj_in.data_time,
            cargo_type_id=obj_in.cargo_type_id,
            route_id=obj_in.route_id,
            weight=obj_in.weight,
            volume=obj_in.volume,
            amount=obj_in.amount,
            source_id=obj_in.source_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deleteAll(self, db: Session) -> Any:
        rows_delete = db.query(BuilkWorks).delete()
        return {"msg": f"удалено строк - {rows_delete}"}


builk_works = CRUDBuilkWork(BuilkWorks)
