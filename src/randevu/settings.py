from split_settings.tools import include

from randevu.conf.environ import env


SECRET_KEY = env('SECRET_KEY', cast=str, default='s3cr3t')

ENVIRONMENT = env('ENVIRONMENT', default='QA')
DEBUG = env('DEBUG', cast=bool, default=False)
ANONYMIZE_ENABLED = DEBUG

# Application definition

try:
    import jupyterlab
    notebook_default_url = '/lab'  # Using JupyterLab
except ImportError:
    notebook_default_url = '/tree'  # Using Jupyter

NOTEBOOK_ARGUMENTS = [
    '--ip', 'localhost',
    '--port', '8888',
    '--notebook-dir', '../',
    '--NotebookApp.default_url', notebook_default_url,
]
IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'
DJANGO_ALLOW_ASYNC_UNSAFE = True

include(
    'conf/api.py',
    'conf/auth.py',
    'conf/boilerplate.py',
    'conf/db.py',
    'conf/debug_toolbar.py',
    'conf/email.py',
    'conf/features.py',
    'conf/http.py',
    'conf/i18n.py',
    'conf/installed_apps.py',
    'conf/media.py',
    'conf/middleware.py',
    'conf/static.py',
    'conf/templates.py',
    'conf/timezone.py',
    'conf/schedule.py',
    'conf/log.py',
    'conf/sentry.py'
)

include('conf/integrations/*.py')
