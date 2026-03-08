# === BUILDER =========================================================
FROM python:3.12-slim AS builder
WORKDIR /app

# Установим build deps (для numpy, psycopg2, pydantic-core, orjson etc.)
RUN apt-get update && apt-get install -y \
        build-essential \
        gcc \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Устанавливаем зависимости в отдельную директорию
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY app ./app


# === FINAL IMAGE =====================================================
FROM python:3.12-slim
WORKDIR /app

# production deps only
COPY --from=builder /install /usr/local

# наш код
COPY --from=builder /app /app

# безопасность и размер
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "app.main"]
