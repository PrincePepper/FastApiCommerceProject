# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.builk_works import *  # noqa
from app.models.cargo_types import *  # noqa
from app.models.database_properties import *  # noqa
# from app.models.object import *  # noqa
from app.models.indicators import *  # noqa
from app.models.road_points import *  # noqa
from app.models.routes import *  # noqa
from app.models.session_histories import *  # noqa
from app.models.sources import *  # noqa
from app.models.users import Users  # noqa
