from fastapi import APIRouter

from app.api.api_v1.routers import utils, user, token, indicators, builk_work, database, source

api_router = APIRouter()

api_router.include_router(token.router, prefix="/token", tags=["login token"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(indicators.router, prefix="/indicators", tags=["indicators"])
api_router.include_router(builk_work.router, prefix="/builk_work",
                          tags=["builk work"])
api_router.include_router(source.router, prefix="/source", tags=["source"])
api_router.include_router(database.router, prefix="/database",
                          tags=["database"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
