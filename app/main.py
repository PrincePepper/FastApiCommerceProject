from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.api_v1.api import api_router
from app.core.config import settings

tags_metadata = [
    {
        'name': 'login token',
        'description': 'Общие манипуляции с токеном',
    },
    {
        'name': 'user',
        'description': 'CRUD функции над пользователем'
    },
    {
        'name': 'users function',
        'description': 'Манипуляции над пользователями'
    },
    {
        'name': 'indicators',
        'description': 'CRUD функции над индикаторами и его смежностями'
    },
    {
        'name': 'builk work',
        'description': 'Работа с данными над источниками'
    },
    {
        'name': 'source',
        'description': 'Работа с источниками'
    },
    {
        'name': 'database',
        'description': 'Обновление данных базы данных и healthcheak'
    },
    {
        'name': 'utils',
        'description': 'Работа со стороними API'
    }
]

app = FastAPI(
    title="API",
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="aplha",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redocs",
)

# Установка всех источников с поддержкой CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    generator=lambda: uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response

# обработчик исключений для authjwt
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )