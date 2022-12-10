from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.routes import Routes
from app.schemas.routes import RouteCreate, RouteUpdate


class CRUDRoute(CRUDBase[Routes, RouteCreate, RouteUpdate]):

    def get_by_id(self, db: Session, *, id: str) -> Optional[Routes]:
        return db.query(Routes).filter(Routes.id == id).first()

    def create(self, db: Session, *, obj_in: RouteCreate) -> Routes:
        db_obj = Routes(
            id=obj_in.id,
            name=obj_in.name,
            from_id=obj_in.from_id,
            to_id=obj_in.to_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


route = CRUDRoute(Routes)
