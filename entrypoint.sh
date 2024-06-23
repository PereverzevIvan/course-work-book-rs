#!/bin/bash -x

cd ./book_rs
touch db.sqlite3 || exit 1
python manage.py migrate --noinput || exit 1
python manage.py loaddata fixtures/users.json || exit 1
python manage.py loaddata fixtures/rs_dump.json || exit 1
exec "$@"