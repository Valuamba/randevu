from randevu.conf.environ import env

MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = env('MEDIA_ROOT', cast=str, default='media')
