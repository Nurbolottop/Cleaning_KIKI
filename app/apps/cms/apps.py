from django.apps import AppConfig


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cms'
    verbose_name = "1) Основные параметры"

    def ready(self):
        from django.core.cache import cache
        from django.db.models.signals import post_save, post_delete
        from apps.cms.context_processors import SETTINGS_CACHE_KEY, SERVICES_CACHE_KEY
        from apps.cms.models import Settings
        from apps.extra.models import OurServices

        def _clear_settings_cache(**kwargs):
            cache.delete(SETTINGS_CACHE_KEY)

        def _clear_services_cache(**kwargs):
            cache.delete(SERVICES_CACHE_KEY)

        post_save.connect(_clear_settings_cache, sender=Settings, weak=False)
        post_delete.connect(_clear_settings_cache, sender=Settings, weak=False)
        post_save.connect(_clear_services_cache, sender=OurServices, weak=False)
        post_delete.connect(_clear_services_cache, sender=OurServices, weak=False)
