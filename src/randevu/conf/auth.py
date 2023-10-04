from datetime import timedelta
from randevu.conf.environ import env

AUTH_USER_MODEL = "users.User"


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT"
    ),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'SIGNING_KEY': env("SIGNING_KEY", cast=str),
    'AUTH_HEADER_NAME': "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken", )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
