from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # Importing the signals module from the users app and connecting it to the ready method of the UsersConfig class
    def ready(self):
        import users.signals
