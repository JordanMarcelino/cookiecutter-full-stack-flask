from flask import Blueprint

from flask_login import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/")
@login_required
def home():
    pass
