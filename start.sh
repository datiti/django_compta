#!/bin/bash

# Initialize application (superuser creation, database init, etc...)
echo Initialize...
./init.sh

# Start gunicorn processes
echo Start Gunicorn...
exec gunicorn django_compta.wsgi:application --bind 0.0.0.0:8000 --workers 3
