from django.apps import AppConfig


class UsersappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersApp'
    
    # Connect the signals - now the usersApp knows about the signals.py file and it can actually connect it
    def ready(self):
        import usersApp.signals
