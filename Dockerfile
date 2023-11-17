ARG PYTHON_VERSION=$PYTHON_VERSION

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
    apt-get install -y --no-install-recommends `echo $OS_PACKAGES | sed 's+,+ +g'`

RUN groupadd -g 1001 code && \
    useradd -r -u 1001 -g code code

WORKDIR /code

COPY --chown=code:code ./ .

RUN pip install  --no-cache -r requirements.txt

USER 1001

ENTRYPOINT /usr/local/bin/gunicorn --workers 4 --bind 0.0.0.0:8008 wsgi:app
