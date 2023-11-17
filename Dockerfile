ARG PYTHON_VERSION=3.8

FROM python:$PYTHON_VERSION-slim as builder

ARG OS_PACKAGES=$OS_PACKAGES
ARG DOCKERFILE_PATH=$DOCKERFILE_PATH

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DOCKERFILE_PATH=$DOCKERFILE_PATH \
    OS_PACKAGES=$OS_PACKAGES

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev libpq-dev build-essential

RUN groupadd -g 1001 code && \
    useradd -r -u 1001 -g code code

WORKDIR /code

COPY --chown=code:code requirements.txt .
COPY --chown=code:code upload_s3_db.py .
COPY --chown=code:code config.py .

RUN pip install  --no-cache -r requirements.txt

USER 1001

ENTRYPOINT /usr/local/bin/python upload_s3_db.py
