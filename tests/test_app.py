import pytest
from firstrep.app import create_app

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

def test_home_route(client):
    response = client.get("/")
    assert response.status_code in (200, 302)