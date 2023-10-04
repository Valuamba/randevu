DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "django_countries",
    "phonenumber_field",
    "rest_framework_simplejwt",
    'corsheaders',
    'debug_toolbar',
    "anymail",
    'drf_yasg',
    'django_extensions'
]

LOCAL_APPS = [ 'apps.users', 'apps.multilanding', 'apps.mailing', 
              'apps.locales', 'apps.schedule', 'apps.service', 'apps.client',
              'apps.appointment', 'apps.employee', 'randevu']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS