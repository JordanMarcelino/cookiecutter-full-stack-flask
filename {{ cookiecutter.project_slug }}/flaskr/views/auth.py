from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from flask_jwt_extended import unset_jwt_cookies

import pendulum

from werkzeug.exceptions import InternalServerError

from flaskr.core import confirm_token
from flaskr.core import generate_token
from flaskr.core import get_url
from flaskr.core import logger
from flaskr.core import logout_required
from flaskr.core import post_request
from flaskr.core import send_email
from flaskr.extensions import bcrypt_ext
from flaskr.forms import LoginForm
from flaskr.forms import RegisterForm
from flaskr.schemas import UserRegisterRequest
from flaskr.schemas import UserLoginRequest
from flaskr.repository import user_repository

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        email, password = (
            form.email.data,
            form.password.data,
        )

        req = UserRegisterRequest(email=email, password=password)

        res = post_request(
            get_url(request.base_url, url_for("api_auth.register")),
            payload=req.model_dump(),
        )

        if not res["info"]["success"]:
            logger.error(res)
            raise InternalServerError(description="failed register user")

        user = user_repository.get(res["data"]["id"])

        token = generate_token(user.email)

        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        req = UserLoginRequest(email=email, password=password)
        res = post_request(
            get_url(request.base_url, url_for("api_auth.login")),
            payload=req.model_dump(),
        )

        if res["info"]["success"]:
            flash("A confirmation email has been sent via email.", "success")
            return redirect(url_for("auth.inactive"))
        else:
            logger.error(res)
            abort(500)

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        email, password = form.email.data, form.password.data
        req = UserLoginRequest(email=email, password=password)

        res = post_request(
            get_url(request.base_url, url_for("api_auth.login")),
            payload=req.model_dump(),
        )

        if res["info"]["success"]:
            user = user_repository.get_by_email(email)
            login_user(user)

            if not user.is_confirmed:
                flash("Please confirm your account!", "warning")
                return redirect(url_for("auth.inactive"))

            return redirect(url_for("core.home"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("auth/login.html", form=form)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")

    res = redirect(url_for("auth.login"))
    unset_jwt_cookies(res)

    return res


@auth_bp.route("/confirm/<string:token>")
@login_required
def confirm_email(token: str):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.home"))

    email = confirm_token(token)

    user = user_repository.get_by_email(current_user.email)

    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = pendulum.now().int_timestamp

        user_repository.update(user)

        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("core.home"))


@auth_bp.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for("core.home"))
    return render_template("auth/inactive.html")


@auth_bp.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("core.home"))

    token = generate_token(current_user.email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)

    html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("auth.inactive"))
