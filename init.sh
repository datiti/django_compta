#!/bin/bash


echo Migrate database...
python manage.py migrate

echo Create superuser if not exist
python init_user.py

echo Import data into database...
python manage.py loaddata Account.json
