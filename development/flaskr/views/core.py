from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from flask_jwt_extended import jwt_required

from flaskr.core import check_is_confirmed

core_bp = Blueprint("core", __name__, url_prefix="")


@jwt_required
@core_bp.get("/home")
@login_required
@check_is_confirmed
def home():
    return render_template("core/index.html")
