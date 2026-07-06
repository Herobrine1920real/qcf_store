#!/usr/bin/env bash

pip install -r requirements.txt
pthon manage.py collectstatic --noinput
python manage.py migrate