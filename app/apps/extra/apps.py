from django.apps import AppConfig


class ExtraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.extra'
    verbose_name = "2) Дополнительные параметры"