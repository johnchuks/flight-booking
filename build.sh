#!/usr/bin/env bash

set -e # stops execution on error
python manage.py makemigrations
python manage.py migrate
python manage.py test