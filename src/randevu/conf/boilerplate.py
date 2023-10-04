import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'randevu.urls'

WSGI_APPLICATION = 'randevu.wsgi.application'
