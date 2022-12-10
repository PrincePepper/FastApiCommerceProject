import base64
import hashlib

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from app.core.config import settings

salt = str.encode(settings.SALT_SECRET_KEY)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_token_location: set = {'cookies', 'headers'}
    # # Разрешить отправку файлов cookie JWT только через https
    authjwt_cookie_secure: bool = False
    # # Включите защиту от двойной отправки csrf.
    authjwt_cookie_csrf_protect: bool = False
    #
    # # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # # authjwt_cookie_samesite: str = 'none'
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    key = hashlib.pbkdf2_hmac("sha256", plain_password.encode('utf-8'), salt, 100000)
    return str(key) == hashed_password


def get_password_hash(password: str) -> str:
    key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000)
    return str(key)
