import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_route(client):
    response = client.get("/login")
    assert response.status_code in (200, 302)