#!/bin/sh

set -e
./manage.py migrate

exec uwsgi --http :8000 --module categories_api.wsgi
