from django.conf import settings


def get_db_conf():
    if settings.DATABASES:
        return settings.DATABASES.get('default', {})
    return {}


def get_db_engine():
    db_conf = get_db_conf()
    return db_conf.get('ENGINE', '')


def is_sqlite_db():
    return get_db_engine() == 'django.db.backends.sqlite3'


def get_db_name():
    db_conf = get_db_conf()
    return db_conf.get('NAME', '')
