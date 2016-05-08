#!/bin/bash
pip install -r /usr/src/app/requirements.txt
./manage.py migrate --database=sqlite
./manage.py migrate --database=postgres
./manage.py migrate --database=mysql
exec "$@"