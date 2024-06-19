import json
import sys
from pytest import mark

sys.path.append("..")
from staclint_lambda.staclint_lambda import app
from fastapi.testclient import TestClient

client = TestClient(app)


@mark.post_url
def test_validate_url_post_request_invalid_json() -> None:
    stac_url_json = {
        "url": "https://github.com/radiantearth/stac-spec/blob/master/examples/simple-item.json?raw=true"
    }

    response = client.post("/url", json=stac_url_json)
    response_json = json.loads(response.content.decode())
    assert response.status_code == 422


@mark.post_url
def test_validate_url_post_request_valid_stac() -> None:
    stac_url_json = {
        "stac_url": "https://github.com/radiantearth/stac-spec/blob/master/examples/simple-item.json?raw=true"
    }

    response = client.post("/url", json=stac_url_json)
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]
    assert response.status_code == 200
    assert is_valid_stac


@mark.post_url
def test_validate_url_post_request_invalid_stac() -> None:
    stac_url_json = {
        "stac_url": "https://github.com/radiantearth/stac-spec/blob/master/examples/simple-item.json"
    }
    response = client.post("/url", json=stac_url_json)
    response_json = json.loads(response.content.decode())
    assert response.status_code == 200
    assert "error_message" in response_json["body"].keys()
