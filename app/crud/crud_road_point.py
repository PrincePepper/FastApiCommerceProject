from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.road_points import RoadPoints
from app.schemas.road_points import RoadPointCreate, RoadPointUpdate


class CRUDRoadPoint(CRUDBase[RoadPoints, RoadPointCreate, RoadPointUpdate]):

    def get_by_id(self, db: Session, *, id: str) -> Optional[RoadPoints]:
        return db.query(RoadPoints).filter(RoadPoints.id == id).first()

    def create(self, db: Session, *, obj_in: RoadPointCreate) -> RoadPoints:
        db_obj = RoadPoints(
            id=obj_in.id,
            name=obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


road_point = CRUDRoadPoint(RoadPoints)
