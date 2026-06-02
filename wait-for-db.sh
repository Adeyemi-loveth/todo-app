#!/bin/bash
echo "Waiting for postgres..."
while true; do
  python << 'PYEOF'
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('db', 5432))
    s.close()
    exit(0)
except Exception as e:
    print(f"Not ready: {e}")
    exit(1)
PYEOF
  if [ $? -eq 0 ]; then
    break
  fi
  sleep 2
done
echo "Postgres is ready — starting Gunicorn"
exec gunicorn --bind 0.0.0.0:5000 --workers 3 wsgi:app
