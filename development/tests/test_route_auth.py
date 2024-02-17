from flask.testing import FlaskClient


def test_root_route(client: FlaskClient):
    response = client.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome !" in response.data


def test_logout_route_requires_login(client: FlaskClient):
    response = client.get("/auth/logout", follow_redirects=True)
    assert b"Please log in to access this page", response.data


def test_login_route_get_success(client: FlaskClient):
    response = client.get(
        "/auth/login",
    )

    assert response.status_code == 200
    assert b"Login", response.data


def test_register_route_get_success(client: FlaskClient):
    response = client.get(
        "/auth/register",
    )

    assert response.status_code == 200
    assert b"Signup", response.data
