#!/usr/bin/env python3
"""Собирает все CSS темы в один app/core/static/assets/css/bundle.css.

Запускать из корня проекта после изменения любого из файлов темы:
    python3 scripts/build_css_bundle.py

В бандл входит всё, включая custom.css и responsive.css (в конце каскада).
Если установлен пакет csscompressor, бандл дополнительно минифицируется.
"""
import pathlib
import re

CSS_DIR = pathlib.Path(__file__).resolve().parent.parent / 'app/core/static/assets/css'

ORDER = [
    'bootstrap.min.css', 'animate.min.css', 'custom-animate.css', 'swiper.min.css',
    'font-awesome-all.css', 'jquery.magnific-popup.css', 'odometer.min.css',
    'flaticon.css', 'owl.carousel.min.css', 'owl.theme.default.min.css',
    'nice-select.css', 'aos.css', 'twentytwenty.css',
    'module-css/banner.css', 'module-css/slider.css', 'module-css/footer.css',
    'module-css/sliding-text.css', 'module-css/about.css', 'module-css/services.css',
    'module-css/counter.css', 'module-css/before-and-after.css', 'module-css/office-location.css',
    'module-css/pricing.css', 'module-css/blog.css', 'module-css/newsletter.css',
    'module-css/faq.css', 'module-css/team.css', 'module-css/testimonial.css',
    'module-css/why-choose.css', 'module-css/process.css', 'module-css/project.css',
    'module-css/contact.css', 'module-css/page-header.css', 'module-css/google-map.css',
    'style.css', 'custom.css', 'responsive.css',
]


def main():
    parts = []
    for name in ORDER:
        text = (CSS_DIR / name).read_text(errors='ignore')
        if 'module-css/' in name:
            # относительные url() внутри module-css поднимаем на уровень выше
            def fix(m):
                u = m.group(1).strip('\'" ')
                if u.startswith(('data:', 'http', '/', '#')):
                    return m.group(0)
                return f'url({u[3:]})' if u.startswith('../') else f'url(module-css/{u})'
            text = re.sub(r'url\(([^)]+)\)', fix, text)
        parts.append(f'/* ===== {name} ===== */\n' + text)

    bundle = '\n'.join(parts).replace('font-display: auto', 'font-display: swap')
    try:
        from csscompressor import compress
        bundle = compress(bundle)
        print('minified with csscompressor')
    except ImportError:
        print('csscompressor не установлен — бандл без минификации')
    (CSS_DIR / 'bundle.css').write_text(bundle)
    print(f'bundle.css: {len(bundle) / 1024:.0f} KB from {len(ORDER)} files')


if __name__ == '__main__':
    main()
