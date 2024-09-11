from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    AppConfig for the 'main' Django app.

    Attributes:
        - default_auto_field (str): The name of the default auto-generated primary key field.
        - name (str): The name of the Django app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
