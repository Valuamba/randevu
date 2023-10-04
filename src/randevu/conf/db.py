from randevu.conf.environ import env


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DATABASES = {
    'default': env.db(),    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

if not env('DEBUG', cast=bool):
    DATABASES['default']['CONN_MAX_AGE'] = 600
