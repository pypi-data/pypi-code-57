import django_heroku


def settings(config):
    django_heroku.settings(config)

    # Remove require SSL from database configuration created by django_heroku
    try:
        del config['DATABASES']['default']['OPTIONS']['sslmode']
    except KeyError:
        pass
