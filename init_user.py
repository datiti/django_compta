import configparser
import os
import django


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_compta.settings")
    django.setup()
    from django.contrib.auth.models import User
    if os.path.exists('config.ini'):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            username = config['admin']['username']
            password = config['admin']['password']
            email = config['admin']['email']
            User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)
        except KeyError as err:
            print('Error: config.ini is missing some config variables', err)
    else:
        print('Error: config.ini file does not exist')
