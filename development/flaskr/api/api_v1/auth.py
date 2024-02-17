from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies

import pendulum

from pydantic_core import ValidationError

from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import Unauthorized

from flaskr.core import logger
from flaskr.core import prod_settings
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.schemas import AuthResponse
from flaskr.schemas import UserLoginRequest
from flaskr.schemas import UserRegisterRequest
from flaskr.schemas import UserRegisterResponse
from flaskr.schemas import WebResponse
from flaskr.schemas import Info
from flaskr.repository import user_repository

api_auth_bp = Blueprint(
    "api_auth", __name__, url_prefix=f"{prod_settings.API_V1_STR}/auth"
)


@api_auth_bp.post("/register")
def register():
    try:
        json = request.get_json()

        req = UserRegisterRequest(**json)

        entity = User(email=req.email, password=req.password)

        user_repository.add(entity)

        info = Info(success=True, message="success register user")
        web_response = WebResponse[UserRegisterResponse](
            info=info,
            data=UserRegisterResponse(
                id=entity.get_id(),
                email=entity.email,
                created_at=pendulum.from_timestamp(
                    entity.created_at, tz=pendulum.local_timezone()
                ),
                updated_at=pendulum.from_timestamp(
                    entity.updated_at, tz=pendulum.local_timezone()
                ),
            ),
        )

        return jsonify(web_response.model_dump()), 200
    except (HTTPException, ValidationError) as exc:
        logger.error(exc)

        if isinstance(exc, HTTPException):
            info = Info(success=False, message=exc.description)
            web_response = WebResponse[None](info=info)

            return jsonify(web_response.model_dump()), exc.code
        elif isinstance(exc, ValidationError):
            info = Info(success=False, message="bad request", meta=exc.errors())
            web_response = WebResponse[None](info=info)

            return jsonify(web_response.model_dump()), 400
    except Exception as exc:
        logger.error(exc)

        info = Info(success=False, message="failed register user")
        web_response = WebResponse[None](info=info)

        return jsonify(web_response.model_dump()), 500


@api_auth_bp.post("/login")
def login():
    try:
        json = request.get_json()

        req = UserLoginRequest(**json)

        user = user_repository.get_by_email(req.email)

        if not bcrypt_ext.check_password_hash(user.password, req.password):
            raise Unauthorized(description="password doesn't match")

        access_token = create_access_token(user.id)

        info = Info(success=True, message="success login user")
        res = jsonify(
            WebResponse[AuthResponse](
                info=info,
                data=AuthResponse(
                    id=user.get_id(), email=user.email, token=access_token
                ),
            ).model_dump()
        )

        set_access_cookies(res, access_token)

        return res, 200

    except (HTTPException, ValidationError) as exc:
        logger.error(exc)

        if isinstance(exc, HTTPException):
            info = Info(success=False, message=exc.description)
            web_response = WebResponse[None](info=info)

            return jsonify(web_response.model_dump()), exc.code
        elif isinstance(exc, ValidationError):
            info = Info(success=False, message="bad request", meta=exc.errors())
            web_response = WebResponse[None](info=info)

            return jsonify(web_response.model_dump()), 400

    except Exception as exc:
        logger.error(exc)

        info = Info(success=False, message="failed login")
        web_response = WebResponse[None](info=info)

        return jsonify(web_response.model_dump()), 500
