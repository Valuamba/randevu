from randevu.conf.environ import env


DEBUG = env('DEBUG', cast=bool, default=False)