import os
import json
import sys
from pytest import mark

sys.path.append("..")
from staclint_lambda.staclint_lambda import app
from fastapi.testclient import TestClient

client = TestClient(app)


@mark.get_url
def test_validate_url_get_request_valid_stac() -> None:
    stac_url = "https://github.com/radiantearth/stac-spec/blob/master/examples/simple-item.json?raw=true"
    response = client.get(
        "/url?stac_url=%s" % stac_url,
    )
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]

    assert response.status_code == 200
    assert is_valid_stac


@mark.get_url
def test_validate_url_get_request_invalid_stac() -> None:
    stac_url = "https://github.com/radiantearth/stac-spec/blob/master/examples/simple-item.json"
    response = client.get(
        "/url?stac_url=%s" % stac_url,
    )
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]
    stac_error_type = response_json["body"]["error_type"]

    assert response.status_code == 200
    assert not is_valid_stac
    assert "JSONDecodeError" in stac_error_type
