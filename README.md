# An accounting application for personal use

## Administration tasks

* Create locales for french and english
```
python manage.py makemessages -l fr
python manage.py makemessages -l en
```
* Update i18n files
```
python manage.py makemessages --all
```
* Compile i18n files (*.po)
```
python manage.py compilemessages
```
* Update database with current models (create migrations file then migrate db)
```
python manage.py makemigrations
python manage.py migrate
```
* Create superuser
```
python manage.py createsuperuser
```
