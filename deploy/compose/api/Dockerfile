FROM python:3.12.1-slim-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./poetry.lock ./
RUN pip install --no-cache-dir --upgrade pip==24.0 \
    && pip install --no-cache-dir setuptools==69.5.1 wheel==0.43.0 \
    && pip install --no-cache-dir poetry==1.8.2 \
    && poetry install --only main \
    && apt-get purge -y gcc git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
    

FROM python-base AS production
WORKDIR /src

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./src/ /src/

EXPOSE 8000
