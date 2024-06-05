#!/bin/sh

# wait-for-it.sh
# Use this script to test if a given TCP host/port are available

set -e

host="$SQL_HOST"
port="$SQL_PORT"

until nc -z -v -w30 "$host" "$port"; do
  echo "Waiting for database connection at $host:$port..."
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Apply database migrations
python manage.py migrate

# Start server
exec "$@"
