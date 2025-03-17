#!/bin/bash

set -e

# Функция для проверки доступности PostgreSQL
function postgres_ready(){
python << END
import sys
import psycopg2
import os

try:
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host="db"
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

# Ожидание запуска PostgreSQL
until postgres_ready; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "PostgreSQL is available"

# Запуск миграций
echo "Applying migrations..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"