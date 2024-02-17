from typing import Union

from itsdangerous import URLSafeTimedSerializer

from flaskr.core import prod_settings


def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(prod_settings.SECRET_KEY)
    return serializer.dumps(email, salt=prod_settings.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600) -> Union[str, bool]:
    serializer = URLSafeTimedSerializer(prod_settings.SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt=prod_settings.SECURITY_PASSWORD_SALT, max_age=expiration
        )
        return email
    except Exception:
        return False
