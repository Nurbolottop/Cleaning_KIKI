import os

from django import template

register = template.Library()


@register.filter
def mobile_image_url(field):
    """URL мобильной версии картинки (<name>_m.<ext>), если она существует.

    Мобильные версии генерируются в Slide.save(); если файла нет —
    возвращаем оригинал, ничего не ломается.
    """
    try:
        base, ext = os.path.splitext(field.path)
        if os.path.exists(base + '_m' + ext):
            url_base, url_ext = os.path.splitext(field.url)
            return url_base + '_m' + url_ext
    except Exception:
        pass
    try:
        return field.url
    except Exception:
        return ''
