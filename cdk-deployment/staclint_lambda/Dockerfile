FROM lambci/lambda:build-python3.8

WORKDIR /code

COPY . /code/

RUN mkdir -p /asset && \
	python -m pip install --upgrade pip && \
	pip install mangum uvicorn fastapi[all]==0.99.1 stac_check stac_validator jsonschema==4.17.3 -t /asset

RUN pip install /code -t /asset

RUN cp /code/cdk-deployment/staclint_lambda/staclint_lambda.py /asset/staclint_lambda.py

CMD ["echo", "hello world"]