from randevu.conf.environ import env

EMAIL_ENABLED = env('EMAIL_ENABLED', cast=bool, default=False)

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

DEFAULT_FROM_EMAIL = env('EMAIL_FROM', cast=str, default='')
ANYMAIL = {
    'POSTMARK_SERVER_TOKEN': env('POSTMARK_SERVER_TOKEN', cast=str, default=''),
    'DEBUG_API_REQUESTS': env('DEBUG'),
}

VERIFY_ACCOUNT_TEMPLATE_ID = env('VERIFY_ACCOUNT_TEMPLATE_ID', cast=str, default='verify-account')
PASSWORD_RESET_TEMPLATE_ID = env('PASSWORD_RESET_TEMPLATE_ID', cast=str, default='password-reset')
NEW_EMPLOYEE_TEMPLATE_ID = env('NEW_EMPLOYEE_TEMPLATE_ID', cast=str, default='new-employee')
