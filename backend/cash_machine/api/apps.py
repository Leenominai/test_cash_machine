from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Конфигурация приложения API.

    Attributes:
        default_auto_field (str): Имя класса для использования в качестве
            автоматического поля при создании моделей.
        name (str): Имя приложения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
