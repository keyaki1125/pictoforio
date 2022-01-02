from django.apps import AppConfig


class MyAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myAccount'

    def ready(self):
        from . import signals