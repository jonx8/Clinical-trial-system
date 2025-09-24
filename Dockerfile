FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential libffi-dev curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --root-user-action=ignore poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

RUN useradd -m appuser

USER appuser


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
