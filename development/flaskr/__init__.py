from datetime import datetime
from datetime import timedelta
from typing import Any

from flask import Flask
from flask import Response
from flask import render_template

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

from pydantic_settings import BaseSettings

from flaskr.core import logger
from flaskr.core import DevelopmentSettings
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.extensions import csrf
from flaskr.extensions import db
from flaskr.extensions import login_manager
from flaskr.extensions import mail
from flaskr.extensions import jwt
from flaskr.views import auth_bp


def create_app(config: BaseSettings = DevelopmentSettings()) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        bcrypt_ext.init_app(app)
        csrf.init_app(app)
        db.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
        jwt.init_app(app)

        app.register_blueprint(auth_bp, prefix="/auth")

        try:
            db.create_all()
        except:
            logger.error("Error creating table schemas")

    @login_manager.user_loader
    def load_user(user_id: str) -> Any:
        return User.query.filter(User.id == user_id).first()

    @app.after_request
    def refresh_expiring_jwts(response: Response) -> Response:
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now()
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    @app.route("/")
    def root():
        return render_template("base.html")

    return app
