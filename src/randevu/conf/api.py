from datetime import timedelta

from randevu.conf.environ import env


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'randevu.pagination.AppPagination',
    # 'EXCEPTION_HANDLER': 'app.sentry_exception_handler.sentry_exception_handler',
    # 'PAGE_SIZE': 20,
}