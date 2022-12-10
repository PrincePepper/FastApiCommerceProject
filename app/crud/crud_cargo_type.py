from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cargo_types import CargoTypes
from app.schemas.cargo_types import CargoTypeCreate, CargoTypeUpdate


class CRUDRoadPoint(CRUDBase[CargoTypes, CargoTypeCreate, CargoTypeUpdate]):

    def get_by_id(self, db: Session, *, id: str) -> Optional[CargoTypes]:
        return db.query(CargoTypes).filter(CargoTypes.id == id).first()

    def create(self, db: Session, *, obj_in: CargoTypeCreate) -> CargoTypes:
        db_obj = CargoTypes(
            id=obj_in.id,
            name=obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


cargo_types = CRUDRoadPoint(CargoTypes)
