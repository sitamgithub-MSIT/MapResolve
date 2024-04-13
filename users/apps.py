from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig for the users app.

    This class defines the configuration for the users app, including the default auto field and the name of the app.
    It also imports the signals module from the users app and connects it to the ready method of the UsersConfig class.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # Importing the signals module from the users app and connecting it to the ready method of the UsersConfig class
    def ready(self):
        import users.signals
