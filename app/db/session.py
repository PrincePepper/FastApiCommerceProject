import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

from app.core import config
from app.core.config import settings


def _build_async_db_uri(uri):
    if "+asyncpg" not in uri:
        return '+asyncpg:'.join(uri.split(":", 1))
    return uri

    # Настройка подключения к базе данных через SSH или без


def connect_sqlalc(ssh=False):
    global ssh_tunnel

    print('\nПопытка подключения к базе данных...\n')

    if ssh:
        try:
            ssh_tunnel = SSHTunnelForwarder(
                settings.SSH_HOST,
                ssh_username=settings.SSH_USER,
                ssh_private_key=settings.SSH_PRIVATE_KEY,
                ssh_private_key_password=settings.SSH_PRIVATE_KEY_PASSWORD,
                remote_bind_address=settings.SSH_ROMOTE_BIND_ADDRESS
            )

            ssh_tunnel.start()
        except:
            print("Подключение по SSH провалено")
            return 0

    database_url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        host=settings.POSTGRES_SERVER_HOST,
        port=ssh_tunnel.local_bind_port if ssh else settings.POSTGRES_SERVER_PORT,
        user=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        db=settings.POSTGRES_DATABASE
    )
    settings.SQLALCHEMY_DATABASE_URI = database_url
    engine = create_engine(config.settings.SQLALCHEMY_DATABASE_URI, echo=True)

    def timer(timeout):
        Timer = threading.Timer(timeout, helthcheck)
        Timer.start()

    def helthcheck():
        with engine.begin() as ddd:
            ddd.in_transaction()
    try:
        print(timer(2))
    except:
        print("База данных не существует или неверно введенные данные")
        print("\nПопытка подключения провалено...\n")
    else:
        print("\nК базе данных поключено...\n")
    return engine


engine = connect_sqlalc(False)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)

# engine = create_async_engine(_build_async_db_uri(settings.SQLALCHEMY_DATABASE_URI))
# async_session = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )
#
# CACHE = {}
# async def _load_all():
#     global CACHE
#     try:
#         async with async_session() as session:
#             q = select(TableClass)
#             result = await session.execute(q)
#             curr = result.scalars()
#             CACHE = {i.id: i.alias for i in curr}
#     except:
#         pass
#
# LOOP.run_until_complete(_load_all())

# https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database
