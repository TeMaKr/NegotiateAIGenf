from fastapi import Depends
from fastapi.testclient import TestClient

from api import app
from security.api_token import check_api_token
from settings import settings

settings.fastapi_api.token = "valid_token"


@app.get("/secret", dependencies=[Depends(check_api_token)])
async def read_secret_path():
    return {"secret": "Hello World"}


client = TestClient(app)


def test_missing_header():
    response = client.get(
        url="/secret",
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "API token is required."}


def test_invalid_token():
    response = client.get(
        url="/secret",
        headers={"X-API-Token": "invalid_token"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API token."}


def test_valid_token():
    response = client.get(
        url="/secret",
        headers={"X-API-Token": "valid_token"},
    )
    assert response.status_code == 200
    assert response.json() == {"secret": "Hello World"}
