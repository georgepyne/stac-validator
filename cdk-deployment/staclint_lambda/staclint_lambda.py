import json
import tempfile
from typing import Dict
import requests
from requests.exceptions import MissingSchema, JSONDecodeError
from stac_check import lint
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from stac_validator import stac_validator
from starlette.responses import JSONResponse
from pydantic import BaseModel

# this is used to push to aws cdk with prod endpoint
app = FastAPI(title="STAC Validator", version=2.0)


class StacURL(BaseModel):
    stac_url: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate(stac_object_dict: Dict | str):
    try:
        linter = lint.Linter(stac_object_dict)
        lint_result = linter.create_best_practices_dict()
        output = linter.message
        output["lint"] = lint_result
        print(lint_result)
    except KeyError as e:
        # If JSON parsed and stac is invalid
        # use stac validator lib for validation
        temp_stac_file = tempfile.NamedTemporaryFile(
            delete=False,
            mode="w+",
        )
        json.dump(stac_object_dict, temp_stac_file)
        temp_stac_file.flush()
        temp_stac_file.close()
        stac = stac_validator.StacValidate(temp_stac_file.name)
        stac.run()
        output = stac.message[0]
    return output


@app.get("/")
async def homepage():
    return {"body": "https://api.staclint.com/docs"}


@app.get("/url")
async def validate_url_get_request(stac_url):
    try:
        response = requests.get(stac_url)
        # process stac url
        output = validate(response.json())
        print(output)
        return {"body": output}
    except (MissingSchema, ValueError, JSONDecodeError, KeyError) as e:
        return JSONResponse(
            status_code=200,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e.__class__),
                    "error_message": str(e),
                }
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e.__class__),
                    "error_message": str(e),
                }
            },
        )


@app.post("/url")
async def validate_url_post_request(stac_url_object: StacURL):
    try:
        stac_url_json = stac_url_object
        stac_url = stac_url_json.stac_url
        request = requests.get(stac_url)
        stac_object_dict = request.json()
        output = validate(stac_object_dict)
        return {"body": output}
    except (MissingSchema, ValueError, JSONDecodeError, KeyError) as e:
        return JSONResponse(
            status_code=200,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e.__class__),
                    "error_message": str(e),
                }
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e),
                    "error_message": str(e),
                }
            },
        )


@app.post("/json")
async def validate_json(request: Request):
    try:
        stac_object_dict = await request.json()
        output = validate(stac_object_dict)
        return {"body": output}
    except (MissingSchema, ValueError, JSONDecodeError, KeyError) as e:
        return JSONResponse(
            status_code=200,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e.__class__),
                    "error_message": str(e),
                }
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "body": {
                    "version": "",
                    "path": "",
                    "schema": [""],
                    "valid_stac": False,
                    "error_type": str(e.__class__),
                    "error_message": str(e),
                }
            },
        )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="STAC Validator",
        description="API for validating STAC files. Powered by Sparkgeo.",
        version=2.0,
        routes=app.routes,
    )
    openapi_schema["paths"]["/json"]["post"] = {
        "description": "This endpoint supports validation of STAC JSON directly. Post your data as JSON.",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
handler = Mangum(app)
