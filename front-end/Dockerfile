FROM python:3.9-slim

LABEL name="valheim-webserver"
LABEL author="Eric Cotner"
LABEL github_handle="ecotner"

SHELL [ "/bin/bash" , "-l", "-c"]
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT flask run --host=0.0.0.0 --port=${FLASK_PORT}