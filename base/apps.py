from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    AppConfig for the 'base' app.

    This class defines the default_auto_field and name attributes for the 'base' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
