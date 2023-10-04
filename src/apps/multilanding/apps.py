from django.apps import AppConfig


class MultilandingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.multilanding'
    
    # def ready():
    #     user_registered.connect(register_subdomain)
