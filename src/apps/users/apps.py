from django.apps import AppConfig
# from djoser.signals import user_registered
    

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    # def ready(self):
    #     from . import signals
    #     user_registered.connect(signals.my_callback)
