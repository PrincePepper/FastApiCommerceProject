from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import crud_user
from app.db import base  # noqa: F401
from app.schemas import UserCreate


def init_db(db: Session) -> None:

    user = crud_user.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True,
            is_active=True,
            name="admin"
        )
        user = crud_user.user.create(db, obj_in=user_in)  # noqa: F841
