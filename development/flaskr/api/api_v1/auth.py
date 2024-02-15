from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request

from flaskr.core import logger
from flaskr.entity import User
from flaskr.models import AuthResponse
from flaskr.models import UserLoginRequest
from flaskr.models import UserLoginRequest
from flaskr.models import UserRegisterRequest
from flaskr.models import UserRegisterResponse
from flaskr.models import WebResponse
from flaskr.models import Info
from flaskr.repository import user_repository

api_auth_bp = Blueprint("api_auth", __name__)


@api_auth_bp.post("/auth/register")
def register():
    try:
        json = request.json()

        req = UserRegisterRequest(**json)

        entity = User(**req)

        user_repository.add(entity)

        info = Info(success=True, message="success register user")
        web_response = WebResponse(
            info=info,
            data=UserRegisterResponse(
                entity.email, entity.created_at, entity.updated_at
            ),
        )

        return jsonify(web_response), 200
    except Exception as exc:
        logger.error(exc)

        info = Info(success=False, message="failed register user")
        web_response = WebResponse(info=info)

        return jsonify(web_response), 500
