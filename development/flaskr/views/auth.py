from flask import Blueprint
from flask import render_template
from flask import request

from flask_login import login_required

from flaskr.forms import LoginForm
from flaskr.forms import RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    return render_template("auth/register.html", form=form)


@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    return render_template("auth/login.html", form=form)
