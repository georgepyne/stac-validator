FROM lambci/lambda:build-python3.8

WORKDIR /code

COPY . /code/

RUN mkdir -p /asset && \
	python -m pip install --upgrade pip && \
	pip install mangum pytest uvicorn fastapi[all]==0.99.1 stac_check stac_validator jsonschema==4.17.3 -t /asset

RUN pip install /code -t /asset

RUN cp /code/cdk-deployment/aws_lambda/aws_lambda.py /asset/aws_lambda.py

CMD ["echo", "hello world"]