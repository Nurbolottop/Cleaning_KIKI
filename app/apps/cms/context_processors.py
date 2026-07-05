from django.core.cache import cache

SETTINGS_CACHE_KEY = 'site_settings'
SERVICES_CACHE_KEY = 'site_services'
CACHE_TTL = 300  # секунд; кэш также сбрасывается сигналами при изменении в админке


def site_settings(request):
    """Глобальный контекст: настройки сайта и список услуг.

    Нужен на каждой странице (шапка, подвал, сайдбар-форма брони),
    поэтому кэшируется, чтобы не ходить в БД на каждый запрос.
    """
    from apps.cms.models import Settings
    from apps.extra.models import OurServices

    settings_obj = cache.get(SETTINGS_CACHE_KEY)
    if settings_obj is None:
        settings_obj = Settings.objects.first()
        if settings_obj is not None:
            cache.set(SETTINGS_CACHE_KEY, settings_obj, CACHE_TTL)

    services = cache.get(SERVICES_CACHE_KEY)
    if services is None:
        services = list(OurServices.objects.prefetch_related('points'))
        cache.set(SERVICES_CACHE_KEY, services, CACHE_TTL)

    return {
        'settings': settings_obj,
        'services': services,
    }
