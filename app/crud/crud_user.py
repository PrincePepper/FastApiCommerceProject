from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def get_by_id(self, db: Session, *, id: str) -> Optional[Users]:
        return db.query(Users).filter(Users.id == id).first()

    def get_similar_users(self, db: Session, name: str) -> List[Users]:
        return db.query(Users).filter(Users.name.contains(name)).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            password=str(get_password_hash(obj_in.password)),
            name=obj_in.name,
            is_admin=obj_in.is_admin,
            country_code=obj_in.country_code
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_user(
            self, db: Session, *, db_obj: Users, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Users]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_admin(self, user: Users) -> bool:
        return user.is_admin

    def is_active(self, user: Users) -> bool:
        return user.is_active


user = CRUDUser(Users)
