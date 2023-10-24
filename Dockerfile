FROM python:3.10-slim

RUN mkdir -p /app/src

WORKDIR /app

RUN pip install -U pip && pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry check

RUN poetry install

COPY src /app/src/
COPY alembic.ini /app/
COPY migrations /app/migrations

EXPOSE 8000

CMD ["uvicorn", "src.api:server", "--host", "0.0.0.0"]
