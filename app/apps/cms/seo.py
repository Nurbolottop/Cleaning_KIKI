"""SEO-вьюхи: sitemap.xml и robots.txt (без django.contrib.sitemaps,
чтобы не тянуть sites framework и лишние миграции)."""

from django.http import HttpResponse
from django.urls import reverse

from apps.cms.models import Blog
from apps.extra.models import OurServices

SITE_URL = 'https://cleaningkiki.kg'


def sitemap_xml(request):
    static_pages = [
        ('index', 'daily', '1.0'),
        ('services', 'weekly', '0.9'),
        ('about', 'monthly', '0.8'),
        ('contacts', 'monthly', '0.8'),
        ('team', 'monthly', '0.6'),
        ('blog', 'weekly', '0.7'),
        ('booking_form', 'monthly', '0.8'),
        ('testimonial_form', 'monthly', '0.5'),
    ]

    urls = []
    for name, changefreq, priority in static_pages:
        urls.append(
            f"<url><loc>{SITE_URL}{reverse(name)}</loc>"
            f"<changefreq>{changefreq}</changefreq>"
            f"<priority>{priority}</priority></url>"
        )

    for service in OurServices.objects.only('id'):
        urls.append(
            f"<url><loc>{SITE_URL}{reverse('services_details', args=[service.id])}</loc>"
            f"<changefreq>monthly</changefreq><priority>0.8</priority></url>"
        )

    for post in Blog.objects.only('id', 'created_at'):
        urls.append(
            f"<url><loc>{SITE_URL}{reverse('blog_details', args=[post.id])}</loc>"
            f"<lastmod>{post.created_at:%Y-%m-%d}</lastmod>"
            f"<changefreq>yearly</changefreq><priority>0.6</priority></url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(urls) +
        '</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /ckeditor/\n"
        "Allow: /\n"
        f"\nSitemap: {SITE_URL}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')
