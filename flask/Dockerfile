ARG PYTHON_VERSION=3.8

FROM python:$PYTHON_VERSION-slim as builder

ENV PIP_DEFAULT_TIMEOUT=1000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev libpq-dev build-essential

RUN groupadd -g 1001 ws && \
    useradd -r -u 1001 -g ws ws

RUN mkdir /ws && chown ws:ws /ws

WORKDIR /ws

COPY --chown=ws:ws . /ws/

RUN pip install  --no-cache -r requirements.txt

USER 1001

ENTRYPOINT /usr/local/bin/gunicorn --workers 4 --bind 0.0.0.0:8008 wsgi:app
