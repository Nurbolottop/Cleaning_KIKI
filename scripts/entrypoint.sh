#!/bin/sh
set -e

# Ожидание доступности базы данных
echo "Ожидание доступности базы данных..."
until nc -z -w5 "$POSTGRES_HOST" "$POSTGRES_PORT"
do
  echo "Waiting for PostgreSQL database connection..."
  sleep 1
done

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Собираем статические файлы..."
python manage.py collectstatic --noinput

# Запускаем переданную команду
exec "$@"
