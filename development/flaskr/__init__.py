from datetime import datetime
from datetime import timedelta
from typing import Any

from flask import Flask
from flask import Response
from flask import render_template

from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies

from flaskr.api.api_v1 import api_auth_bp
from flaskr.core import dev_settings
from flaskr.core import logger
from flaskr.core import prod_settings
from flaskr.core import Settings
from flaskr.entity import User
from flaskr.extensions import bcrypt_ext
from flaskr.extensions import csrf
from flaskr.extensions import db
from flaskr.extensions import limiter
from flaskr.extensions import login_manager
from flaskr.extensions import mail
from flaskr.extensions import mode
from flaskr.extensions import jwt
from flaskr.repository import user_repository
from flaskr.views import auth_bp
from flaskr.views import core_bp


def create_app(
    config: Settings = prod_settings if mode == "production" else dev_settings,
) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)

    with app.app_context():
        CORS(
            app,
            resources={
                # update to FE or production link
                r"/*": {"origins": ["http://localhost:5000", "https://example.com"]}
            },
        )

        bcrypt_ext.init_app(app)
        csrf.init_app(app)
        db.init_app(app)
        limiter.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
        jwt.init_app(app)

        app.register_blueprint(core_bp)
        app.register_blueprint(api_auth_bp)
        app.register_blueprint(auth_bp)

        csrf.exempt(api_auth_bp)

        try:
            db.create_all()

            # Add admin user
            user_repository.add(
                User(
                    email="superuser@gmail.com",
                    password="root",
                    is_admin=True,
                    is_confirmed=True,
                )
            )
        except Exception as exc:
            logger.error(exc)

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

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("errors/405.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    @app.get("/")
    def root():
        return render_template("index.html")

    return app


app = create_app()
