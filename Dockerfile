FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    awscli \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.6.1
RUN pip install poetry==${POETRY_VERSION}

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    awscli \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY . .

RUN mkdir -p src/localstack-data

CMD ["python", "main.py"]
