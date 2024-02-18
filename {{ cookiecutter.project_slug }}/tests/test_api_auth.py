from flask.testing import FlaskClient

from flaskr.extensions import bcrypt_ext
from flaskr.schemas import UserLoginRequest
from flaskr.schemas import UserRegisterRequest


def test_register_success(client: FlaskClient):
    payload = UserRegisterRequest(
        email="test@gmail.com",
        password="secret",
    )
    response = client.post(
        "/api/v1/auth/register",
        json=payload.model_dump(),
        follow_redirects=True,
    )

    json = response.get_json()

    assert response.status_code == 200
    assert json["info"]["success"] is True
    assert json["info"]["message"] == "success register user"
    assert json["data"]["email"] == "test@gmail.com"


def test_register_failed_invalid_email_format(client: FlaskClient):
    response = client.post(
        "/api/v1/auth/register",
        json=dict(
            email="test",
            password="secret",
        ),
        follow_redirects=True,
    )

    json = response.get_json()

    assert response.status_code == 400
    assert json["info"]["success"] is False
    assert json["data"] is None


def test_login_success(client: FlaskClient):
    payload = UserLoginRequest(
        email="unconfirmeduser@gmail.com",
        password="unconfirmed",
    )
    response = client.post(
        "/api/v1/auth/login",
        json=payload.model_dump(),
        follow_redirects=True,
    )
    json = response.get_json()

    assert response.status_code == 200
    assert json["info"]["success"] is True
    assert json["info"]["message"] == "success login user"
    assert json["data"]["email"] == "unconfirmeduser@gmail.com"


def test_login_failed_wrong_password(client: FlaskClient):
    payload = UserLoginRequest(
        email="unconfirmeduser@gmail.com",
        password="wrong",
    )
    response = client.post(
        "/api/v1/auth/login",
        json=payload.model_dump(),
        follow_redirects=True,
    )

    json = response.get_json()

    assert response.status_code == 401
    assert json["info"]["success"] is False
    assert json["info"]["message"] == "password doesn't match"


def test_login_failed_user_not_found(client: FlaskClient):
    payload = UserLoginRequest(
        email="notexist@gmail.com",
        password="secret",
    )
    response = client.post(
        "/api/v1/auth/login",
        json=payload.model_dump(),
        follow_redirects=True,
    )

    json = response.get_json()

    print(json)
    assert response.status_code == 404
    assert json["info"]["success"] is False
    assert "not found" in json["info"]["message"]


def test_login_failed_invalid_email_format(client: FlaskClient):
    response = client.post(
        "/api/v1/auth/login",
        json=dict(
            email="test",
            password="secret",
        ),
        follow_redirects=True,
    )

    json = response.get_json()

    assert response.status_code == 400
    assert json["info"]["success"] is False
    assert json["data"] is None
