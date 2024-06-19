import os
import json
import sys
from pytest import mark

sys.path.append("..")
from staclint_lambda.staclint_lambda import app
from fastapi.testclient import TestClient

client = TestClient(app)


@mark.post_json
def test_validate_json_valid_stac() -> None:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "test-stac-item.json"), "r") as f:
        valid_stac_item = json.load(f)

    response = client.post("/json", json=valid_stac_item)
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]

    assert response.status_code == 200
    assert is_valid_stac


@mark.post_json
def test_validate_json_invalid_stac() -> None:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "test-stac-item.json"), "r") as f:
        invalid_stac_item = json.load(f)
    invalid_stac_item.pop("id")
    response = client.post("/json", json=invalid_stac_item)
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]
    stac_error_type = response_json["body"]["error_type"]
    print(stac_error_type)
    assert response.status_code == 200
    assert not is_valid_stac
    assert "JSONSchemaValidationError" in stac_error_type


@mark.post_json
def test_validate_json_invalid_lint() -> None:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "test-stac-item.json"), "r") as f:
        stac_item = json.load(f)

    response = client.post("/json", json=stac_item)
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]

    assert response.status_code == 200
    assert is_valid_stac
    assert response_json["body"]["lint"]


@mark.post_json
def test_validate_json_valid_lint() -> None:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "test-stac-item.json"), "r") as f:
        stac_item = json.load(f)
    stac_item["id"] = stac_item["id"].lower()
    response = client.post("/json", json=stac_item)
    response_json = json.loads(response.content.decode())
    is_valid_stac = response_json["body"]["valid_stac"]

    assert response.status_code == 200
    assert is_valid_stac
    assert not response_json["body"]["lint"]
