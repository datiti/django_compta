# An accounting application for personal use

This django application aims at providing a basic accounting application 
for single person professional (eg: lawyer, developer with his own company, etc...).

It does provide i18n (international translation) support for english (en)
and french (fr): see below in admin section for howto create internationalization 
files.

It currently uses a local sqlite3 database engine: in future release, 
PostgreSQL will be the standard database.

You can initialize the database with several accounts; there is a default fixture
file for this: compta/fixtures/Account.json.

Why 'compta' for the name? compta is the french word for accounting :)

All the needed requirements are in 'requirements.txt' file, you can install
using pip:
    pip install -r requirements.txt

There is already an experimental support of Docker (see Dockerfile for more details):
you can find it at Docker hub [django-python36](https://hub.docker.com/r/datiti/django-python36/)

## What to expect in the coming releases ?

* support of PostgreSQL database engine to secure data storage
* use of docker-compose to run as 2 docker containers: one for the database
and one for the django application
* support of a full rest api to interact with the application
* support mobile UI (currently in development) using reactive framework

## Running the application

If you want to use the 'start.sh' starting script, you should first create a
config.ini file taking example from config.ini.sample: basically, it contains
the admin user, password and email to connect to the admin interface.

If under Linux, you can use the start.sh file to start the application using 
gunicorn.

    ./start.sh

This script invokes 'init.sh' script that does:
* database migration if needed
* verify that superuser exists, if not it will create it
* initialize the database data with accounts defined in compta/fixtures/Account.json

## Docker deployment

You can look at the Dockerfile to have more details.

### To build the container image

    docker build -t datiti/django-compta .


### To remove the container before running the update of the image
    docker rm compta


### To run the container image
    docker run -d -p 127.0.0.1:8000:8000 --name compta datiti/django-compta
In this example:

* -d indicates to detach from terminal
* -p 127.0.0.1:8000:8000 indicates to bind the local host 127.0.0.1 and port 8000 to the container port 8000
* –name compta indicates that the container will be named compta
* datiti/django-compta is the name of the image to run


## Administration tasks

### Create locales for french and english
    python manage.py makemessages -l fr
    python manage.py makemessages -l en
### Update i18n files
    python manage.py makemessages --all

### Compile i18n files (*.po)
    python manage.py compilemessages

### Update database with current models (create migrations file then migrate db)
    python manage.py makemigrations
    python manage.py migrate

### Create superuser
    python manage.py createsuperuser

### Create db backup
    python manage.py dbbackup

### To list db backups
    python manage.py listbackups
