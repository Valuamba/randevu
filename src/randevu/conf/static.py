import os.path

from randevu.conf.boilerplate import BASE_DIR
from randevu.conf.environ import env

STATIC_URL = env('STATIC_URL', default='/superstatic/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
